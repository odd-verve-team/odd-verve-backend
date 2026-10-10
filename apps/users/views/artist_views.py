from rest_framework import generics

from apps.users.models import ArtistProfile
from apps.users.serializers import (
    ArtistProfileListSerializer,
    ArtistProfileDetailSerializer,
)


class ArtistProfileListView(generics.ListAPIView):
    queryset = ArtistProfile.objects.select_related("artist").all()
    serializer_class = ArtistProfileListSerializer


class ArtistProfileDetailView(generics.RetrieveAPIView):
    queryset = ArtistProfile.objects.select_related("artist").all()
    serializer_class = ArtistProfileDetailSerializer
