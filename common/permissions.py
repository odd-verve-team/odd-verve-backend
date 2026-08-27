import functools
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from apps.authentication.jwt import decode_token

def get_current_user_payload(request):
    """
    Хелпер для витягування payload з JWT токена (HttpOnly Cookie або Authorization Header).
    """
    token = request.COOKIES.get(settings.JWT_AUTH_COOKIE)
    
    if not token:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

    if not token:
        return None

    try:
        payload = decode_token(token, expected_type='access')
        return payload
    except Exception:
        return None


def login_required(view_func):
    """
    Декоратор для перевірки авторизації користувача.
    """
    @functools.wraps(view_func)
    def wrapper(self_or_request, *args, **kwargs):
        request = self_or_request if hasattr(self_or_request, 'COOKIES') else args[0] if args else None
        if not request and hasattr(self_or_request, 'request'):
            request = self_or_request.request

        payload = get_current_user_payload(request)
        if not payload:
            return Response(
                {"detail": "Автентифікація обов'язкова. Будь ласка, увійдіть у систему."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        request.user_id = payload.get('sub')
        request.user_role = payload.get('role')
        return view_func(self_or_request, *args, **kwargs)

    return wrapper


def roles_required(*allowed_roles):
    """
    Декоратор для обмеження доступу за ролями (наприклад: @roles_required('admin', 'artist')).
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(self_or_request, *args, **kwargs):
            request = self_or_request if hasattr(self_or_request, 'COOKIES') else args[0] if args else None
            if not request and hasattr(self_or_request, 'request'):
                request = self_or_request.request

            payload = get_current_user_payload(request)
            if not payload:
                return Response(
                    {"detail": "Автентифікація обов'язкова."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            user_role = payload.get('role')
            if user_role not in allowed_roles:
                return Response(
                    {"detail": "У вас немає достатньо прав для виконання цієї дії."},
                    status=status.HTTP_403_FORBIDDEN
                )

            request.user_id = payload.get('sub')
            request.user_role = user_role
            return view_func(self_or_request, *args, **kwargs)

        return wrapper
    return decorator