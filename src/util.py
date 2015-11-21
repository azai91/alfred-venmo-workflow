import json

def validate_amount(amount):
    # if '.' in amount and more stuff after period:
    #     return False
    try:
        return '{:.2f}'.format(float(amount))
    except:
        return False

def create_post_message(friend):
    try:
        friend = json.loads(friend)
    except:
        pass

    display_name = friend['display_name']
    amount = friend['amount']
    note = friend['note']

    return "%s received $%s for %s" % (display_name, amount, note)

def format_amount(amount):
    """
    Formats user input amount

    Args:
        amount, a user inputted value

    Returns:
        a string formatted as such, $x.xx or -$x.xx

    """

    amount = validate_amount(amount)
    return '$%s' % amount if amount[0] != '-' else '-$%s' % amount[1:]

