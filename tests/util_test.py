"""
Unit tests for util library
"""

import json
import src.util as util
import unittest
from tests.sample_data import sample_friends

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

        with self.assertRaises(ValueError):
            util.validate_amount('-')
            util.validate_amount('f')
            util.validate_amount('1f')
            util.validate_amount('10.f')
            util.validate_amount('10.0f')


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

    def test_generate_payload(self):
        """
        Test generate_payload method

        generate_payload generates transaction payload from user inputted string
        """

        # must be first friend
        friend = sample_friends[0]

        self.assertEqual(util.generate_payload([''], friend), {
            'user_id' : friend['id'],
            'amount' : '[amount]',
            'note' : '[note]',
            'display_name' : friend['display_name']
            })

        self.assertEqual(util.generate_payload(['1'], friend), {
            'user_id' : friend['id'],
            'amount' : '1.00',
            'note' : '[note]',
            'display_name' : friend['display_name']
            })

        self.assertEqual(util.generate_payload(['-'], friend), {
            'user_id' : friend['id'],
            'amount' : '[amount]',
            'note' : '[note]',
            'display_name' : friend['display_name']
            })

        self.assertEqual(util.generate_payload(['1', ''], friend), {
            'user_id' : friend['id'],
            'amount' : '1.00',
            'note' : '[note]',
            'display_name' : friend['display_name']
            })

        self.assertEqual(util.generate_payload(['1', 't'], friend), {
            'user_id' : friend['id'],
            'amount' : '1.00',
            'note' : 't',
            'display_name' : friend['display_name']
            })

        self.assertEqual(util.generate_payload(['1', 'test test'], friend), {
            'user_id' : friend['id'],
            'amount' : '1.00',
            'note' : 'test test',
            'display_name' : friend['display_name']
            })

    def test_format_title(self):
        """
        Test format_title method

        format_title takes dictionary with transaction information and returns a
        properly formatted string to be displayed in feedback
        """

        # must be first friend
        friend = sample_friends[0]

        payload = {
            'user_id' : friend['id'],
            'amount' : '[amount]',
            'note' : '[note]',
            }
        self.assertEqual(util.format_title(payload, friend),
                         '%s [amount] [note]' % friend['display_name'])

        payload = {
            'user_id' : friend['id'],
            'amount' : '1.00',
            'note' : '[note]',
            }
        self.assertEqual(util.format_title(payload, friend),
                         'pay %s $1.00 [note]' % friend['display_name'])

        payload = {
            'user_id' : friend['id'],
            'amount' : '-1.00',
            'note' : '[note]',
            }
        self.assertEqual(util.format_title(payload, friend),
                         'charge %s $1.00 [note]' % friend['display_name'])

        payload = {
            'user_id' : friend['id'],
            'amount' : '-1.00',
            'note' : 't',
            }
        self.assertEqual(util.format_title(payload, friend),
                         'charge %s $1.00 for t' % friend['display_name'])


if __name__ == '__main__':
    unittest.main()
