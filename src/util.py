import json

def validate_amount(amount):
    # if '.' in amount and more stuff after period:
    #     return False
    try:
        return "{:.2f}".format(float(amount))
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

    return "%s sent to %s for %s" % (amount, display_name, note)