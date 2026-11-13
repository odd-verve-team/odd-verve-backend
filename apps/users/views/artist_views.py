from rest_framework import generics

from apps.users.models import Profile
from apps.users.serializers import (
    ArtistProfileListSerializer,
    ArtistProfileDetailSerializer,
)


class ArtistProfileListView(generics.ListAPIView):
    queryset = Profile.objects.select_related("artist").all()
    serializer_class = ArtistProfileListSerializer


class ArtistProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.select_related("artist").all()
    serializer_class = ArtistProfileDetailSerializer
