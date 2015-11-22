"""
Venmo API
"""

import requests
import sys
import subprocess
import json
from config import CLIENT_ID, CLIENT_SECRET, AUTH_URL, TOKEN_URL, FRIENDS_URL, CACHE_MAX_AGE, PAYMENTS_URL, LOGOUT, LOGIN, CLEAR_CACHE, INVALID
from workflow import Workflow, ICON_WARNING
import random, string
import urllib
import util

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-venmo-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-venmo-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

class Venmo:

    @classmethod
    def open_auth_page(cls):
        """
        Opens the authorization page
        """

        cls.start_auth_server()
        subprocess.call(['open', AUTH_URL])

    @classmethod
    def start_auth_server(cls):
        """
        Starts server to capture code from redirect uri
        """

        subprocess.Popen(['nohup','python','./server.py'])

    @classmethod
    def exchange_token(cls, code):
        """
        Exchanges code for access_token

        Args:
            code, a string of the code generated from the authorization page.

        Returns:
            response, dict, a dictionary holding the response from the Venmo server.
        """

        response = requests.post(TOKEN_URL, {
            'code': code,
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET,
        }).json()

        return response

    @classmethod
    def save_credentials(cls, credentials):
        """
        Save tokens and user information from response

        Args:
            credentials, dict, a dictionary holding the acceess token, refresh token, and user information.
        """

        wf.save_password('venmo_access_token', credentials['access_token'])
        wf.save_password('venmo_refresh_token', credentials['refresh_token'])

        # stores user information
        wf.store_data('venmo_user', credentials['user'])

    @classmethod
    def delete_credentials(cls):
        """
        Deletes venmo access_token
        """

        wf.delete_password('venmo_access_token')
        wf.delete_password('venmo_refresh_token')

    @classmethod
    def refresh(cls):
        """
        Refreshes tokens
        """

        refresh_token = wf.get_password('venmo_refresh_token')
        response = requests.post(TOKEN_URL, {
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET,
            'refresh_token' : refresh_token,
        }).json()
        wf.save_password('venmo_access_token', response['access_token'])
        wf.save_password('venmo_refresh_token', response['refresh_token'])

    @classmethod
    def get_friends(cls):
        """
        Retreives user's friends

        Returns:
            Array of user's friends
        """

        access_token = wf.get_password('venmo_access_token')
        user = wf.stored_data('venmo_user')
        response = requests.get(FRIENDS_URL % (user['username'], access_token)).json()
        return response['data']

    @classmethod
    def show_filtered_friends(cls, user_input):
        """
        Display list of friends from user input

        Args:
            user_input, user inputted string in Alfred bar.
        """

        try:
            friends = cls.findFriends(user_input)
            cls.show_friends(friends)
        except:
            wf.add_item(
                title='No friends found',
                icon=ICON_WARNING)

        wf.send_feedback()

    @classmethod
    def show_friends(cls, friends):
        """
        Display list of friends

        Args:

        """

        for index, friend in enumerate(friends):
            title = friend['display_name']
            wf.add_item(
                title=title,
                autocomplete='%s ' % title)

    @classmethod
    def findFriends(cls, user_name):
        """
        Find friend in cached friend's list

        Args:
            user_name, a user inputted string

        Returns:
            an array of all users whose name matches input
        """

        cache_length = CACHE_MAX_AGE
        if not wf.get_password('venmo_access_token'):
            raise Exception('No access token found')

        try:
            cache_length = wf.stored_data('venmo_cache_length') if wf.stored_data('venmo_cache_length') else cache_length
        except:
            pass

        friends = wf.cached_data('venmo_api_results', cls.get_friends, cache_length)
        return [friend for friend in friends if friend['display_name'].lower().startswith(user_name.lower()) or user_name.lower().startswith(friend['display_name'].lower())]

    @classmethod
    def show_options(cls, user_input):
        """
        Display options

        Args:
            user_input, user inputted string in Alfred bar.
        """

        if 'login'.startswith(user_input):
            cls.show_login()
        if 'logout'.startswith(user_input):
            cls.show_logout()
        if 'clear cache'.startswith(user_input):
            cls.show_clear_cache()

        if len(wf._items) == 0:
            cls.show_invalid_option()

        wf.send_feedback()

    @classmethod
    def show_login(cls):
        """
        Display login option
        """

        wf.add_item(title=LOGIN['title'],
            arg=LOGIN['arg'],
            icon=LOGIN['icon'],
            autocomplete=LOGIN['autocomplete'],
            valid=True)

    @classmethod
    def show_logout(cls):
        """
        Display logout option
        """

        wf.add_item(title=LOGOUT['title'],
            arg=LOGOUT['arg'],
            autocomplete=LOGOUT['autocomplete'],
            icon=LOGOUT['icon'],
            valid=True)

    @classmethod
    def show_clear_cache(cls):
        """
        Display clear cache option
        """

        wf.add_item(title=CLEAR_CACHE['title'],
            arg=CLEAR_CACHE['arg'],
            autocomplete=CLEAR_CACHE['autocomplete'],
            icon=CLEAR_CACHE['icon'],
            valid=True)

    @classmethod
    def show_invalid_option(cls):
        """
        Display invalid option
        """

        wf.add_item(title=INVALID['title'],
            icon=ICON_WARNING)

    @classmethod
    def add_update(cls):
        """
        Display update option
        """

        wf.add_item(
            'New version available!',
            'Action this item to install the update',
            autocomplete='workflow:update')

    @classmethod
    def clear_cache(cls):
        """
        Clear cache
        """

        wf.clear_cache()

    @classmethod
    def set_cache_length(cls, length):
        """
        Set cache length
        """

        wf.store_data('venmo_cache_length', length)

    @classmethod
    def complete_transaction(cls, user):
        """
        Sends payment request to venmo server

        Args:
            user, a json string with the user_id, amount, note
        """

        access_token = wf.get_password('venmo_access_token')
        user = json.loads(user)
        audience = 'public' # todo: make input
        url = PAYMENTS_URL % (access_token, user['user_id'], user['note'], user['amount'], audience)
        return requests.post(url)

    @classmethod
    def show_formatting(cls, user_input):
        """
        Displays options based on user input

        Args:
            user_input, a user inputted string
        """

        #removes username from user input
        friend = cls.findFriends(user_input)[0]
        friend_name = friend['display_name']
        rest = user_input[len(friend_name):]
        rest = rest.strip().split(' ', 1)

        if len(rest[0]) and rest[0] != '-' and not util.validate_amount(rest[0]):
            wf.add_item(title='Please insert properly formatted amount')
            return wf.send_feedback()

        payload = cls.generate_payload(rest, friend)
        title = cls.format_title(payload, friend)
        isValid = payload['amount'] != '[amount]' and payload['note'] != '[note]'

        wf.add_item(title=title,
            arg=json.dumps(payload),
            valid=isValid)
        wf.send_feedback()

    @classmethod
    def format_title(cls, payload, friend):
        """
        Creates a string that will be printed in the workflow

        Args:
            payload, a dictonary contains information about transaction
            friend, a dictionary containing information about friend

        Returns:
            a string that will be displayed in workflow

        """

        friend_name = friend['display_name']
        for_prefix = 'for ' if payload['note'] != '[note]' else ''
        action = 'charge ' if payload['amount'].startswith('-') else 'pay ' if payload['amount'] != '[amount]' else ''
        amount = '$%s' % payload['amount'][1:] if payload['amount'].startswith('-') else '$%s' % payload['amount'] if payload['amount'] != '[amount]' else payload['amount']

        title = '%s%s %s %s%s' % (action, friend_name, amount, for_prefix, payload['note'])
        return title

    @classmethod
    def generate_payload(cls, user_input, friend):
        """
        Generate dictionary that contains information about transaction

        Args:
            user_input, a list containing user inputted amount and note
                Ex:
                    ['1']
                    ['1.0', 'hi']

            friend, a dictionary with information about friend

        Returns:
            a dictionary containing properties related to transaction

        """

        amount = util.validate_amount(user_input[0]) or '[amount]'

        try:
            note = user_input[1] or '[note]'
        except:
            note = '[note]'

        return {
            'user_id' : friend['id'],
            'amount' : amount,
            'note' : note,
            'display_name' : friend['display_name']
        }
