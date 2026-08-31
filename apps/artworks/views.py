from rest_framework import generics

from apps.artworks.models import Artwork
from apps.artworks.serializers import ArtworkListSerializer


class ArtworkListView(generics.ListAPIView):
    serializer_class = ArtworkListSerializer
    queryset = Artwork.objects.all().select_related("artist")

    def get_queryset(self):
        is_featured = self.request.query_params.get("is_featured")
        if is_featured.lower() == "true":
            return self.queryset.filter(is_featured=True)
        return self.queryset
