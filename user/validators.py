import re
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

def phone_validator(value):
    pattern = r"09\d{9}$"

    if not re.match(pattern,value):
        raise ValidationError("please enter correct format ex 0912***2029")
    return value

def check_user_not_exists(value):
    user = get_user_model().objects.filter(phone=value)
    if user:
        raise ValidationError("user with this phone already exists")
    return value