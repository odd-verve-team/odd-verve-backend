from rest_framework import generics

from apps.favorites.models import Favorite
from apps.favorites.serializers import (
    FavoriteListSerializer,
    FavoriteCreateSerializer,
    FavoriteDeleteSerializer,
)


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteListSerializer

    def get_queryset(self):
        queryset = Favorite.objects.select_related("artwork", "profile")
        return queryset.filter(profile=self.request.user.profile.id)


class FavoriteCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.select_related("artwork", "profile").all()
    serializer_class = FavoriteCreateSerializer


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.select_related("artwork", "profile").all()
    serializer_class = FavoriteDeleteSerializer

    def get_queryset(self):
        queryset = Favorite.objects.select_related("artwork", "profile")
        return queryset.filter(profile=self.request.user.profile.id)
