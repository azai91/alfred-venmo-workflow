"""
Unit tests of vemno
"""

# pylint: disable=protected-access,

import unittest
import sys
from src.config import LOGIN, LOGOUT, INVALID, CLEAR_CACHE
import os
from src.venmo import main
from src.venmo_api import wf

class TestVenmo(unittest.TestCase):
    """
    Unit tests of venmo
    """

    def test_settings(self):
        """
        Test if settings are displayed properly
        """

        wf._items = []
        sys.argv = ['venmo.py', '>']
        main(None)
        self.assertEqual(len(wf._items), 3)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[1].title, LOGOUT['title'])
        self.assertEqual(wf._items[2].title, CLEAR_CACHE['title'])
        wf._items = []

    def test_invalid_options(self):
        """
        Test if invalid option items is displayed
        """
        wf._items = []

        sys.argv = ['venmo.py.py', '> not here']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, INVALID['title'])
        self.assertFalse(wf._items[0].valid)
        self.assertFalse(wf._items[0].arg)
        wf._items = []

    def test_login(self):
        """
        Test if login item is displayed
        """
        sys.argv = ['venmo.py.py', '> login']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '>login']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '>  login']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '>  Login']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '>  LOGIN']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

    def test_logout(self):
        """
        Test if logout item is displayed properly
        """

        wf._items = []

        sys.argv = ['venmo.py.py', '> logout']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '>logout']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '>  logout']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '>  Logout']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '>  LOGOUT']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

    def test_clear_cache(self):
        """
        Test if clear cache item is displayed properly
        """

        wf._items = []

        sys.argv = ['venmo.py.py', '> cl']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[0].arg, CLEAR_CACHE['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '> clear C']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[0].arg, CLEAR_CACHE['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '>cl']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[0].arg, CLEAR_CACHE['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['venmo.py.py', '> clear cache']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[0].arg, CLEAR_CACHE['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

    def setUp(self):
        # supress stdout of feedback
        sys.stdout = open(os.devnull, 'w')

if __name__ == '__main__':
    unittest.main()
