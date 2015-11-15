import requests
import sys
import subprocess
import json
from config import CLIENT_ID, CLIENT_SECRET, AUTH_URL, TOKEN_URL, FRIENDS_URL, CACHE_MAX_AGE, PAYMENTS_URL
from workflow import Workflow, ICON_ACCOUNT, ICON_EJECT, ICON_BURN, ICON_CLOCK, ICON_WARNING
import random, string
import urllib
import util

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-venmo-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-venmo-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

class Venmo:

    @classmethod
    def open_auth_page(cls):
        cls.start_auth_server()
        subprocess.call(['open', AUTH_URL])

    @classmethod
    def start_auth_server(cls):
        subprocess.Popen(['nohup','python','./server.py'])

    @classmethod
    def exchange_tokens(cls, code):
        response = requests.post(TOKEN_URL, {
            'code': code,
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET,
        }).json()
        return response


    @classmethod
    def save_credentials(cls, credentials):
        wf.save_password('venmo_access_token', credentials['access_token'])
        wf.save_password('venmo_refresh_token', credentials['refresh_token'])

        # stores user information
        wf.store_data('venmo_user', credentials['user'])

    @classmethod
    def get_request_token(cls):
        cls.start_server()
        subprocess.call(['open', cls.get_auth_url()])

    @classmethod
    def delete_credentials(cls):
        wf.delete_password('venmo_access_token','')

    @classmethod
    def refresh(cls):
        refresh_token = wf.get_password('venmo_refresh_token')
        try:
            response = requests.post(TOKEN_URL, {
                'client_id' : CLIENT_ID,
                'client_secret' : CLIENT_SECRET,
                'refresh_token' : refresh_token,
            }).json()
            wf.save_password('venmo_access_token', response['access_token'])
            return 1
        except:
            wf.logger.error('Error Refreshing')
            return 0

    @classmethod
    def get_friends(cls):
        access_token = wf.get_password('venmo_access_token')
        user = wf.stored_data('venmo_user')
        response = requests.get(FRIENDS_URL % (user['username'], access_token)).json()
        # if 'error' in response and cls.refresh():
        #     return cls.get_links()
        # else:
        return response['data']

    @classmethod
    def open_page(cls,url):
        subprocess.call(['open',url])

    @classmethod
    def revoke_token(cls):
        access_token = wf.save_password('access_token','')
        return requests.get('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)

    @classmethod
    def show_friends(cls, user_input):
        cache_length = 0 #change back later
        if not wf.get_password('venmo_access_token'):
            raise Exception('No access token found')
        if wf.stored_data('venmo_cache_length'):
            cache_length = wf.stored_data('venmo_cache_length')

        friends = wf.cached_data('venmo_api_results', cls.get_friends) #add cachge back later
        try:
            friends = wf.filter(query=user_input.lower(), items=friends, key=lambda x : x['display_name'].lower())
        except:
            friends = []

        if len(friends):
            add_items(friends)
        else:
            wf.add_item(
                title='No friends found',
                icon=ICON_WARNING)

        wf.send_feedback()

    @classmethod
    def show_options(cls, user_input):
        if user_input in 'login':
            cls.show_login()
        ## add another condition
        if user_input in 'logout':
            cls.show_logout()
        if user_input in 'clear cache':
            cls.show_clear_cache()
        if user_input[:16] in 'set cache length':
            cls.show_set_cache_length(user_input[17:])
        wf.send_feedback()

    @classmethod
    def show_login(cls):
        wf.add_item(title='d > login',
            arg='login',
            icon=ICON_ACCOUNT,
            autocomplete='> login',
            valid=True)

    @classmethod
    def show_logout(cls):
        wf.add_item(title='d > logout',
            arg='logout',
            autocomplete='> logout',
            icon=ICON_EJECT,
            valid=True)

    @classmethod
    def show_clear_cache(cls):
        wf.add_item(title='d > clear cache',
            arg='clear',
            autocomplete='> clear cache',
            icon=ICON_BURN,
            valid=True)

    @classmethod
    def show_set_cache_length(cls, length):
        if not len(length):
            wf.add_item(title='d > set cache length [seconds]',
                autocomplete='> set cache length ',
                icon=ICON_CLOCK)
        else:
            try:
                int(length)
                wf.add_item(title='d > set cache length %s seconds' % length,
                    arg='set' + length,
                    icon=ICON_CLOCK,
                    valid=True)
            except:
                wf.add_item(title='please insert valid cache length',
                    icon=ICON_CLOCK)

    @classmethod
    def add_update(cls):
        wf.add_item(
            'New version available!',
            'Action this item to install the update',
            autocomplete='workflow:update')

    @classmethod
    def clear_cache(cls):
        wf.clear_cache()

    @classmethod
    def set_cache_length(cls, length):
        wf.store_data('cache_length', length)

    """

    Accepts:
        String, a json with the user_id, note, amount

    """
    @classmethod
    def charge_user(cls, input):
        access_token = wf.get_password('venmo_access_token')
        input = json.loads(input)
        user_id = input['user_id']
        note = input['note']
        amount = input['amount']
        audience = 'public' # todo: make input
        url = PAYMENTS_URL % (access_token, user_id, note, amount, audience)
        body = {
            'user_id' : user_id
        }
        return requests.post(url, body).json()

    @classmethod
    def hasFriend(cls, user_input):
        friends = wf.cached_data('venmo_api_results', cls.get_friends) #get frome
        return [friend for friend in friends if user_input.startswith(friend['display_name'])]

    @classmethod
    def show_formatting(cls, user_input):
        # rename
        friend = cls.hasFriend(user_input)[0]
        friend_name = friend['display_name']
        rest = user_input[len(friend_name):]
        rest = rest.strip().split(' ', 1)

        #refactor
        try:
            amount = rest[0] if len(rest[0]) else '[amount]'
        except:
            amount = '[amount]'

        if amount != '[amount]' and not util.validate_amount(amount):
            wf.add_item(title='Please insert properly formatted amount')
            return wf.send_feedback()
        elif amount!= '[amount]':
            amount = util.validate_amount(amount)

        try:
            note = rest[1]
        except:
            note = '[note]'

        isValid = amount != '[amount]' and note != '[note]'
        title = '%s %s %s' % (friend_name, amount, note)

        payload = {
            'user_id' : friend['id'],
            'amount' : amount,
            'note' : note,
            'display_name' : friend['display_name']
        }

        wf.add_item(title=title,
            arg=json.dumps(payload),
            valid=isValid)
        wf.send_feedback()

def add_items(links):
    # sorted(links, key=lambda link : link['lastViewedByMeDate'])
    for index, link in enumerate(links):
        title = link['display_name']
        icon = link['profile_picture_url']
        wf.add_item(
            title=title,
            autocomplete='%s ' % title)