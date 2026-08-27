from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config.database import SessionLocal
from apps.users.models import User
from apps.authentication.jwt import decode_token
from django.conf import settings

class ProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get(settings.JWT_AUTH_COOKIE)
        if not token:
            return Response({"detail": "Неавторизований"}, status=status.HTTP_401_UNAUTHORIZED)
        
        payload = decode_token(token)
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == payload['sub']).first()
            if not user:
                return Response({"detail": "Користувача не знайдено"}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                "id": user.id,
                "email": user.email,
                "fullName": user.full_name,
                "role": user.role.value,
                "avatarUrl": user.avatar_url
            })
        finally:
            db.close()