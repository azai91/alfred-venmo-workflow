"""
Unit tests for util library
"""

import json
import src.util as util
import unittest

class TestUtil(unittest.TestCase):
    """
    Unit test util library
    """

    def test_validate_amount(self):
        """
        Test validate_amount function in util library

        validate_amount returns properly formatted currency or False if string formmated
        improperly
        """

        self.assertEqual(util.validate_amount('1'), '1.00')
        self.assertEqual(util.validate_amount('10'), '10.00')
        self.assertEqual(util.validate_amount('10.'), '10.00')
        self.assertEqual(util.validate_amount('10.0'), '10.00')
        self.assertEqual(util.validate_amount('10.00'), '10.00')
        self.assertFalse(util.validate_amount('-'))
        self.assertFalse(util.validate_amount('f'))
        self.assertFalse(util.validate_amount('1f'))
        self.assertFalse(util.validate_amount('10.f'))
        self.assertFalse(util.validate_amount('10.0f'))


    def test_create_post_message(self):
        """
        Test create_post_message function in util library

        create_post_message takes a properly formatted json string and return formatted
        string for push notification
        """

        sample_friend = json.dumps({
            'display_name' : 'Test',
            'amount' : '12.00',
            'note' : 'test'
        })
        self.assertEqual(str(util.create_post_message(sample_friend)),
                         'Test received $12.00 for test')

        sample_friend = json.dumps({
            'display_name' : 'Test',
            'amount' : '-12.00',
            'note' : 'test'
        })
        self.assertEqual(str(util.create_post_message(sample_friend)),
                         'Test was charged $12.00 for test')

    def test_format_amount(self):
        """
        Test format_amount function in util library

        format_amount converts string to dollar formatted string
        """

        self.assertEqual(util.format_amount('1'), '$1.00')
        self.assertEqual(util.format_amount('-1'), '$1.00')
        self.assertEqual(util.format_amount('1.'), '$1.00')
        self.assertEqual(util.format_amount('-1.'), '$1.00')
        self.assertEqual(util.format_amount('1.0'), '$1.00')
        self.assertEqual(util.format_amount('-1.0'), '$1.00')


if __name__ == '__main__':
    unittest.main()
