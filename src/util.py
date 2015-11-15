
def validate_amount(amount):
    # if '.' in amount and more stuff after period:
    #     return False
    try:
        return "{:.2f}".format(float(amount))
    except:
        return False