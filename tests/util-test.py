"""
Unit tests for util library
"""

import src.util as util
import unittest

class TestUtil(unittest.TestCase):

    def test_validate_amount(self):
        self.assertTrue(util.validate_amount('0'))

if __name__ == '__main__':
    unittest.main()