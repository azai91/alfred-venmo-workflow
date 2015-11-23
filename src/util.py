"""
Basic util library
"""

import json

# pylint: disable= bare-except

def validate_amount(amount):
    """
    Validate user input to float format with two decimal

    Args:
        amount, user input string

    Returns:
        a string in correct format

    """

    return '{:.2f}'.format(float(amount))

def create_post_message(friend):
    """
    Creates message for push notification

    Args:
        friend, a json format string containing transction information

    Returns:
        a string containing message for push notification

    """

    try:
        friend = json.loads(friend)
    except:
        pass

    display_name = friend['display_name']

    # removes negative sign
    amount = friend['amount'] if not friend['amount'][0].startswith('-') else friend['amount'][1:]
    action = 'received' if not friend['amount'].startswith('-') else 'was charged'

    note = friend['note']

    return "%s %s $%s for %s" % (display_name, action, amount, note)

def format_amount(amount):
    """
    Formats user input amount

    Args:
        amount, a user inputted value

    Returns:
        a string formatted as such, $x.xx or -$x.xx

    """

    amount = validate_amount(abs(float(amount)))
    return '$%s' % amount

def generate_payload(user_input, friend):
    """
    Generate dictionary that contains information about transaction

    Args:
        user_input, a list containing user inputted amount and note
            Ex:
                ['1']
                ['1.0', 'hi']

        friend, a dictionary with information about friend

    Returns:
        a dictionary containing properties related to transaction

    """

    try:
        amount = validate_amount(user_input[0])
    except:
        amount = '[amount]'

    try:
        note = user_input[1] or '[note]'
    except:
        note = '[note]'

    return {
        'user_id' : friend['id'],
        'amount' : amount,
        'note' : note,
        'display_name' : friend['display_name'] # for printing out name in push notification
    }

def format_title(payload, friend):
    """
    Creates a string that will be printed in the workflow

    Args:
        payload, a dictonary contains information about transaction
        friend, a dictionary containing information about friend

    Returns:
        a string that will be displayed in workflow

    """

    friend_name = friend['display_name']
    for_prefix = 'for ' if payload['note'] != '[note]' else ''
    action = ''

    if payload['amount'].startswith('-'):
        action = 'charge '
    elif payload['amount'] != '[amount]':
        action = 'pay '

    amount = payload['amount']
    if payload['amount'].startswith('-'):
        amount = '$%s' % payload['amount'][1:]
    elif payload['amount'] != '[amount]':
        amount = '$%s' % payload['amount']

    title = '%s%s %s %s%s' % (action, friend_name, amount, for_prefix, payload['note'])
    return title

