import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.conf import settings
from config.database import SessionLocal
from apps.artworks.models import Artwork, ArtworkStatus
from apps.authentication.jwt import decode_token

class CreateOrderView(APIView):
    def post(self, request):
        token = request.COOKIES.get(settings.JWT_AUTH_COOKIE)
        if not token:
            return Response({"detail": "Створювати замовлення можуть лише авторизовані користувачі"}, status=status.HTTP_401_UNAUTHORIZED)
        
        payload = decode_token(token)
        user_id = payload['sub']
        cart_key = f"cart:user:{user_id}"
        
        cart_data = cache.get(cart_key)
        if not cart_data:
            return Response({"detail": "Кошик порожній"}, status=status.HTTP_400_BAD_REQUEST)
        
        items = json.loads(cart_data)
        db = SessionLocal()
        try:
            total_amount = 0
            for item in items:
                art = db.query(Artwork).filter(Artwork.id == item['artworkId']).first()
                if art:
                    total_amount += float(art.price) * item.get('quantity', 1)
                    art.status = ArtworkStatus.RESERVED  # Резервуємо картину

            db.commit()
            
            # Очищуємо кошик у Redis після замовлення
            cache.delete(cart_key)
            
            order_id = str(uuid.uuid4())
            return Response({
                "orderId": order_id,
                "totalAmount": total_amount,
                "status": "PENDING",
                "message": "Замовлення успішно створене"
            }, status=status.HTTP_201_CREATED)
        finally:
            db.close()