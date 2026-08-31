from rest_framework import generics

from apps.artworks.models import Artwork
from apps.artworks.serializers import ArtworkListSerializer


class ArtworkListView(generics.ListAPIView):
    serializer_class = ArtworkListSerializer

    def get_queryset(self):
        queryset = Artwork.objects.all().select_related("artist")
        is_featured = self.request.query_params.get("is_featured")

        if is_featured and is_featured == "true":
            return queryset.filter(is_featured=True)
        return queryset
