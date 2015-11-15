
def validate_amount(amount):
    # if '.' in amount and more stuff after period:
    #     return False
    try:
        return "{:.2f}".format(float("40.12"))
    except ValueError:
        return False