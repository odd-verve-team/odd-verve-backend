import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def create_tokens(user_id: str, role: str):
    now = datetime.now(timezone.utc)
    
    access_payload = {
        'sub': user_id,
        'role': role,
        'type': 'access',
        'exp': now + settings.ACCESS_TOKEN_LIFETIME,
        'iat': now,
    }
    refresh_payload = {
        'sub': user_id,
        'type': 'refresh',
        'exp': now + settings.REFRESH_TOKEN_LIFETIME,
        'iat': now,
    }

    access_token = jwt.encode(access_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return access_token, refresh_token

def decode_token(token: str, expected_type: str = 'access'):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get('type') != expected_type:
            raise AuthenticationFailed("Некоректний тип токена")
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Термін дії токена закінчився")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Недійсний токен")