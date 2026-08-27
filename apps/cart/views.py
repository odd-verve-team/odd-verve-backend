import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from apps.authentication.jwt import decode_token
from django.conf import settings

def get_cart_key(request):
    token = request.COOKIES.get(settings.JWT_AUTH_COOKIE)
    if token:
        try:
            payload = decode_token(token)
            return f"cart:user:{payload['sub']}"
        except Exception:
            pass
    
    # Якщо неавторизований — кошик прив'язується до session_id з кук
    session_id = request.COOKIES.get('cart_session_id', 'anonymous_guest')
    return f"cart:session:{session_id}"

class CartView(APIView):
    def get(self, request):
        cart_key = get_cart_key(request)
        cart_data = cache.get(cart_key)
        items = json.loads(cart_data) if cart_data else []
        return Response({"items": items})

    def post(self, request):
        cart_key = get_cart_key(request)
        data = request.data  # {"artworkId": "...", "quantity": 1}
        
        cart_data = cache.get(cart_key)
        items = json.loads(cart_data) if cart_data else []
        
        # Додаємо елемент
        items.append({"artworkId": data.get("artworkId"), "quantity": data.get("quantity", 1)})
        cache.set(cart_key, json.dumps(items), timeout=86400 * 7)  # Кеш на 7 днів
        
        return Response({"items": items}, status=status.HTTP_201_CREATED)