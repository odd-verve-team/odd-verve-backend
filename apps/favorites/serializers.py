from rest_framework import serializers

from apps.artworks.serializers import ArtworkListSerializer
from apps.favorites.models import Favorite


class FavoriteListSerializer(serializers.ModelSerializer):
    artwork = ArtworkListSerializer(read_only=True)

    class Meta:
        model = ("id", "profile", "artwork")


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ("artwork",)

    def create(self, validated_data):
        profile = self.context["request"].user.profile.id
        artwork = validated_data["artwork"]
        Favorite.objects.create(profile=profile, artwork=artwork)


class FavoriteDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ()
