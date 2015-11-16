"""
Unit tests for Venmo API
"""

import unittest
import src.venmo_api as venmo_api
# from src.venmo_api import Venmo as Venmo_backup

CachedData = {}
Passwords = {}
StoreData = {}

class TestVenmoAPI(unittest.TestCase):
    def test_get_friends(self):
        friends = venmo_api.Venmo.get_friends()
        self.assertTrue(isinstance(friends, list))


    def test_save_credentials(self):
        pass

    def setUp(self):
        # CachedData.clear()
        # Passwords

        # replaces cache
        def cached_data(self, key, max_age=None):
            return CachedData.get(key)
        venmo_api.Workflow.cached_data = cached_data

        def get_password(self, key):
            return Passwords.get(key)
        venmo_api.Workflow.get_password = get_password

        def delete_password(self, key):
            if key in Passwords:
                del Passwords[key]
        venmo_api.Workflow.delete_password = delete_password

        # def store_data(self, )

if __name__ == '__main__':
    unittest.main()

