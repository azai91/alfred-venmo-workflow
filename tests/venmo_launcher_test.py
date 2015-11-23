"""
Unit tests for launcher
"""

# pylint: disable=invalid-name

import unittest
from src.venmo_api import wf
from src.venmo_launcher import main
import httpretty
from tests.sample_data import sample_friends, sample_user
from src.config import FRIENDS_URL
import json
import os
import sys

SAMPLE_ACCESS_TOKEN = 'test'
CachedData = {}
Passwords = {}
StoredData = {}

class TestVenmoLauncher(unittest.TestCase):
    """Unit tests for Venmo API"""

    @httpretty.activate
    def xtest_login(self):
        """Test login command"""

        sys.argv = ['venmo_launcher.py', 'login']

        httpretty.register_uri(httpretty.GET, FRIENDS_URL %
                               (sample_user['username'], SAMPLE_ACCESS_TOKEN),
                               body=json.dumps({'data' : sample_friends}),
                               content_type='application/json')

    def test_logout(self):
        """Test logout command"""

        sys.argv = ['venmo_launcher.py', 'logout']
        wf.save_password('venmo_access_token', 'access')
        wf.save_password('venmo_refresh_token', 'refresh')

        self.assertEqual(wf.get_password('venmo_access_token'), 'access')
        self.assertEqual(wf.get_password('venmo_refresh_token'), 'refresh')

        main(None)

        self.assertFalse(wf.get_password('venmo_access_token'))
        self.assertFalse(wf.get_password('venmo_token_token'))

    def test_clear_cache(self):
        """Test clear_cache command"""

        sys.argv = ['venmo_launcher.py', 'clear']
        wf.cache_data('venmo_api_results', 'data')
        wf.cache_data('venmo_api_results_backup', 'backup_data')

        self.assertEqual(wf.cached_data('venmo_api_results'), 'data')
        self.assertEqual(wf.cached_data('venmo_api_results_backup'), 'backup_data')

        main(None)

        with self.assertRaises(KeyError):
            wf.cached_data('venmo_api_results')
            wf.cached_data('venmo_api_results_backup')

    def setUp(self):
        sys.stdout = open(os.devnull, 'w')
        # subprocess.call = call

        CachedData.clear()
        StoredData.clear()
        Passwords.clear()

        # replaces cache
        def cached_data(key):
            """Return value in cache"""
            return CachedData[key]

        wf.cached_data = cached_data

        def cache_data(key, value):
            """Save result of calling callback to cache"""
            CachedData[key] = value

        wf.cache_data = cache_data

        def clear_cache():
            """Clear cache"""
            CachedData.clear()

        wf.clear_cache = clear_cache

        def store_data(key, value):
            """Save value in store"""
            StoredData[key] = value

        wf.store_data = store_data

        def stored_data(key):
            """Returns value from store"""
            return StoredData[key]

        wf.stored_data = stored_data

        def save_password(key, value):
            """Save value in password store"""
            Passwords[key] = value

        wf.save_password = save_password

        def get_password(key):
            """Returns value from password store"""
            return Passwords.get(key)

        wf.get_password = get_password

        def delete_password(key):
            """Delete password from password store"""
            if key in Passwords:
                del Passwords[key]

        wf.delete_password = delete_password

        wf.save_password('venmo_access_token', SAMPLE_ACCESS_TOKEN)
        wf.store_data('venmo_user', sample_user)

if __name__ == '__main__':
    unittest.main()

