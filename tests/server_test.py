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

    def test_status(self):
        response = requests.get('http://127.0.0.1:1337')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.text), 'Error with setting code')

        with self.assertRaises(requests.ConnectionError):
            response = requests.get('http://127.0.0.1:1337')


    def setUp(self):
        subprocess.Popen(['nohup','python','./src/server.py'])




if __name__ == '__main__':
    unittest.main()
