import re


def validate_phone_number(v: str):
    if not re.match(r'^\+?[1-9]\d{1,14}$', v):
        raise ValueError('Invalid phone number format')
    return v
