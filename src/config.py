"""
Configurations and constants
"""

# pylint: disable=relative-import

from workflow import ICON_ACCOUNT, ICON_EJECT, ICON_WARNING, ICON_SYNC

CLIENT_ID = '3307'
CLIENT_SECRET = 'S686rq4AAGSXBbgwWJQ3CmhSsfUyFKnY'
SCOPE = 'make_payments access_friends'
REDIRECT_URI = 'http://127.0.0.1:1337'
CACHE_MAX_AGE = 60 * 60 * 24 # one day

AUTH_URL = 'https://api.venmo.com/v1/oauth/authorize?client_id=%s&scope=\
            %s&response_type=code&redirect_uri=%s' % (CLIENT_ID, SCOPE, REDIRECT_URI)
TOKEN_URL = 'https://api.venmo.com/v1/oauth/access_token'
FRIENDS_URL = 'https://api.venmo.com/v1/users/%s/friends?access_token=\
              %s&limit=1000' # need to change limit
PAYMENTS_URL = 'https://api.venmo.com/v1/payments?access_token=%s&user_id=\
               %s&note=%s&amount=%s&audience=%s'

LOGIN = {
    'title' : 'Login',
    'autocomplete' : '> Login',
    'arg' : 'login',
    'icon' : ICON_ACCOUNT
}

LOGOUT = {
    'title' : 'Logout',
    'autocomplete' : '> Logout',
    'arg' : 'logout',
    'icon' : ICON_EJECT
}

CLEAR_CACHE = {
    'title' : 'Clear cache',
    'autocomplete' : '> Clear cache',
    'arg' : 'clear',
    'icon' : ICON_SYNC
}

INVALID = {
    'title' : 'Invalid option',
    'icon' : ICON_WARNING
}

INVALID_FORMAT = {
    'title' : 'Please insert properly formatted amount'
}
