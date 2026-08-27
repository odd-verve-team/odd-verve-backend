import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
import config.database
from apps.artworks.models import Artwork, ArtworkStatus

CACHE_KEY_ARTWORKS = "artworks_catalog_list"

class ArtworkListView(APIView):
    def get(self, request):
        # Перевірка наявності кешу в Redis
        cached_data = cache.get(CACHE_KEY_ARTWORKS)
        if cached_data:
            return Response(json.loads(cached_data))

        db = config.database.SessionLocal()
        try:
            artworks = db.query(Artwork).filter(Artwork.status == ArtworkStatus.AVAILABLE).all()
            result = [
                {
                    "id": art.id,
                    "title": art.title,
                    "description": art.description,
                    "price": float(art.price),
                    "dimensions": art.dimensions,
                    "year": art.year,
                    "technique": art.technique,
                    "images": art.images,
                    "artistId": art.artist_id
                }
                for art in artworks
            ]
            
            # Кешуємо список у Redis на 10 хвилин (600 секунд)
            cache.set(CACHE_KEY_ARTWORKS, json.dumps(result), timeout=600)
            return Response(result)
        finally:
            db.close()