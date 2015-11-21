"""
Unit tests for util library
"""

import json
import src.util as util
import unittest

class TestUtil(unittest.TestCase):

    def test_validate_amount(self):
        self.assertEqual(util.validate_amount('1'),'1.00')
        self.assertEqual(util.validate_amount('10'),'10.00')
        self.assertEqual(util.validate_amount('10.'),'10.00')
        self.assertEqual(util.validate_amount('10.0'),'10.00')
        self.assertEqual(util.validate_amount('10.00'),'10.00')
        self.assertFalse(util.validate_amount('f'))
        self.assertFalse(util.validate_amount('1f'))
        self.assertFalse(util.validate_amount('10.f'))
        self.assertFalse(util.validate_amount('10.0f'))

    def test_create_post_message(self):
        sample_friend = json.dumps({
            'display_name' : 'Test',
            'amount' : '12.00',
            'note' : 'test'
        })
        self.assertEqual(str(util.create_post_message(sample_friend)),'Test received $12.00 for test')

    def test_format_amount(self):
        self.assertEqual(util.format_amount('1'),'$1.00')
        self.assertEqual(util.format_amount('-1'),'-$1.00')
        self.assertEqual(util.format_amount('1.'),'$1.00')
        self.assertEqual(util.format_amount('-1.'),'-$1.00')
        self.assertEqual(util.format_amount('1.0'),'$1.00')
        self.assertEqual(util.format_amount('-1.0'),'-$1.00')



if __name__ == '__main__':
    unittest.main()