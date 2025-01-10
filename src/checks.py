import re


def validate_phone_number(v: str):
    if not re.match(r'^\+?[1-9]\d{1,14}$', v):
        raise ValueError('Invalid phone number format')
    return v


def validate_not_empty_str(v: str, field_name: str):
    if not v.strip():
        raise ValueError(f"The {field_name} value cannot be empty")
    return v


def validate_not_empty(v, field_name: str):
    if not v:
        raise ValueError(f"The {field_name} value cannot be empty")
    return v
