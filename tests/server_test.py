"""
Unit tests for server
"""

import subprocess
import unittest
from src.venmo_api import Workflow, Venmo
import src.httpretty as httpretty
from src.config import TOKEN_URL
import src.requests as requests
import time
# from src.venmo_api import Venmo as Venmo_backup

CachedData = {}
Passwords = {}
StoreData = {}

class TestVenmoAPI(unittest.TestCase):
    # def test_get_friends(self):
    #     friends = Venmo.get_friends()
    #     self.assertTrue(isinstance(friends, list))


    # def test_save_credentials(self):
    #     pass

    # def test_show_friends(self):
    #     pass

    # def test_show_filtered_friends(self):
    #     pass

    # def test_find_friends(self):
    #     pass

    def test_status(self):
        print 'run'
        response = requests.get('http://127.0.0.1:1337/')
        assertTrue(response.status, 200)



    def setUp(self):
        print 'stup'
        Venmo.start_auth_server()
        time.sleep(5)



if __name__ == '__main__':
    unittest.main()

