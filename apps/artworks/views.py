from rest_framework import viewsets

from apps.artworks.models import Artwork
from apps.artworks.serializers import ArtworkListSerializer, ArtworkCreateSerializer


class ArtworkViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            return ArtworkCreateSerializer
        return ArtworkListSerializer

    def get_queryset(self):
        queryset = Artwork.objects.all().select_related("artist")
        is_featured = self.request.query_params.get("is_featured")

        if is_featured and is_featured == "true":
            return queryset.filter(is_featured=True)
        return queryset
