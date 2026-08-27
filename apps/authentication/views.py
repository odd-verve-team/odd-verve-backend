import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

import config.database
from apps.users.models import User, UserRole
from apps.authentication.jwt import create_tokens, decode_token

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        db = config.database.SessionLocal()
        
        try:
            if db.query(User).filter(User.email == data.get('email')).first():
                return Response({"detail": "Користувач вже існує"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User(
                id=str(uuid.uuid4()),
                email=data['email'],
                password_hash=make_password(data['password']),
                full_name=data['fullName'],
                role=data.get('role', UserRole.CUSTOMER)
            )
            db.add(user)
            db.commit()
            return Response({"detail": "Успішно зареєстровано"}, status=status.HTTP_201_CREATED)
        finally:
            db.close()

class LoginView(APIView):
    def post(self, request):
        data = request.data
        db = config.database.SessionLocal()
        try:
            user = db.query(User).filter(User.email == data.get('email')).first()
            if not user or not check_password(data.get('password'), user.password_hash):
                return Response({"detail": "Невірний email або пароль"}, status=status.HTTP_401_UNAUTHORIZED)
            
            access_token, refresh_token = create_tokens(user.id, user.role.value)
            
            response = Response({"detail": "Успішний вхід", "role": user.role.value})
            response.set_cookie(
                key=settings.JWT_AUTH_COOKIE,
                value=access_token,
                httponly=settings.JWT_COOKIE_HTTPONLY,
                secure=settings.JWT_COOKIE_SECURE,
                samesite=settings.JWT_COOKIE_SAMESITE
            )
            response.set_cookie(
                key=settings.JWT_REFRESH_COOKIE,
                value=refresh_token,
                httponly=settings.JWT_COOKIE_HTTPONLY,
                secure=settings.JWT_COOKIE_SECURE,
                samesite=settings.JWT_COOKIE_SAMESITE
            )
            return response
        finally:
            db.close()

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get(settings.JWT_REFRESH_COOKIE)
        if not refresh_token:
            return Response({"detail": "Refresh token відсутній"}, status=status.HTTP_401_UNAUTHORIZED)
        
        payload = decode_token(refresh_token, expected_type='refresh')
        access_token, new_refresh_token = create_tokens(payload['sub'], payload.get('role', 'customer'))
        
        response = Response({"detail": "Токен оновлено"})
        response.set_cookie(key=settings.JWT_AUTH_COOKIE, value=access_token, httponly=True)
        response.set_cookie(key=settings.JWT_REFRESH_COOKIE, value=new_refresh_token, httponly=True)
        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response({"detail": "Успішний вихід"})
        response.delete_cookie(settings.JWT_AUTH_COOKIE)
        response.delete_cookie(settings.JWT_REFRESH_COOKIE)
        return response