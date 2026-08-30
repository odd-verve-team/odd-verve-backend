import re

from django.core.exceptions import ValidationError


def validate_password_complexity(password: str) -> None | ValidationError:
    if len(password) < 8:
        raise ValidationError("Password must contain at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must have at least 1 uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must have at least 1 lowercase letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must have at least 1 digit")
    if not re.search(r"[@$!%*?&#]", password):
        raise ValidationError("Password must have at least 1 special character: @, $, !, %, *, ?, &, #.")
