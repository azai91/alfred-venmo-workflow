"""
Unit tests for Venmo API
"""

import unittest
from src.venmo_api import Workflow, Venmo, wf
import src.httpretty as httpretty
from src.config import TOKEN_URL
from tests.sample_data import sample_friends, sample_user
from src.config import FRIENDS_URL
import json
# from src.venmo_api import Venmo as Venmo_backup

CachedData = {}
Passwords = {}
StoredData = {}

class TestVenmoAPI(unittest.TestCase):

    @httpretty.activate
    def test_get_friends(self):
        sample_access_token = 'test'
        wf.save_password('venmo_access_token', sample_access_token)
        wf.store_data('venmo_user', sample_user)
        httpretty.register_uri(httpretty.GET, FRIENDS_URL % (sample_user['username'], sample_access_token),
            body=json.dumps({"data" : sample_friends }),
            content_type='application/json')

        friends = Venmo.get_friends()
        self.assertTrue(isinstance(friends, list))


    def test_save_credentials(self):
        pass

    def test_show_friends(self):
        pass

    def test_show_filtered_friends(self):
        pass

    @httpretty.activate
    def test_find_friends(self):
        # httpretty.register_uri()

        Venmo.findFriends

    def test_show_options(self):
        pass

    @httpretty.activate
    def test_exchange_token(self):
        httpretty.register_uri(httpretty.POST, TOKEN_URL,
            body='{"access_token" : "string", "user" : {"username": "test"}}',
            content_type='application/json')

        self.assertIsInstance(Venmo.exchange_token('code'), dict)




    def setUp(self):
        CachedData.clear()
        StoredData.clear()
        Passwords.clear()

        # replaces cache
        def cached_data(key, max_age=None):
            return CachedData.get(key)
        wf.cached_data = cached_data

        def store_data(key, value):
            StoredData[key] = value
        wf.store_data = store_data

        def stored_data(key, max_age=None):
            return StoredData[key]
        wf.stored_data = stored_data

        def save_password(key, value):
            Passwords[key] = value
        wf.save_password = save_password

        def get_password(key):
            return Passwords.get(key)
        wf.get_password = get_password

        def delete_password(key):
            if key in Passwords:
                del Passwords[key]
        wf.delete_password = delete_password

        # def store_data(self, )

if __name__ == '__main__':
    unittest.main()

