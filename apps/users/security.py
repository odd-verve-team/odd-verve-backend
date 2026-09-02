import re


def validate_password_complexity(password: str) -> str | None:
    if len(password) < 8:
        return "Password must contain at least 8 characters."
    if not re.search(r"[A-Z]", password):
        return "Password must have at least 1 uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must have at least 1 lowercase letter."
    if not re.search(r"\d", password):
        return "Password must have at least 1 digit"
    if not re.search(r"[@$!%*?&#]", password):
        return (
            "Password must have at least 1 special character: @, $, !, %, *, ?, &, #."
        )
    return None
