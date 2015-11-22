"""
Unit tests of todoist_settings
"""

import unittest
import sys
from src.config import LOGIN, LOGOUT, INVALID, CLEAR_CACHE

from src.venmo import main
from src.venmo_api import wf

class TestVenmo(unittest.TestCase):

    def test_settings(self):
        sys.argv = ['venmo.py','>']
        main(None)
        self.assertEqual(len(wf._items), 3)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[1].title, LOGOUT['title'])
        self.assertEqual(wf._items[2].title, CLEAR_CACHE['title'])
        wf._items = []


    def test_invalid_options(self):
        sys.argv = ['venmo.py.py','not here']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, INVALID['title'])
        self.assertFalse(wf._items[0].valid)
        self.assertFalse(wf._items[0].arg)
        wf._items = []

    def xtest_add_account(self):
        sys.argv = ['venmo.py.py','add']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, 'Add Account')
        self.assertTrue(wf._items[0].valid)
        self.assertTrue(wf._items[0].arg)
        wf._items = []

if __name__ == '__main__':
    unittest.main()