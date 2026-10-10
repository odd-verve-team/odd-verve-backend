from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.artworks.models import Artwork


class ArtistSerializer(serializers.ModelSerializer):
    first_name = serializers.SlugRelatedField(
        many=False,
        slug_field="first_name",
        source="artist_profile"
    )
    last_name = serializers.SlugRelatedField(
        many=False,
        slug_field="last_name",
        source="artist_profile"
    )
    avatar_url = serializers.SlugRelatedField(
        many=False,
        slug_field="avatar_url",
        source="artist_profile"
    )

    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "avatar_url")


class ArtworkListSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()

    class Meta:
        model = Artwork
        fields = "__all__"
        read_only_fields = ("image_width", "image_height")


class ArtworkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = (
            "title",
            "description",
            "category",
            "painting_length",
            "painting_width",
            "price",
            "year",
            "medium",
            "image_url",
        )

    def create(self, validated_data: dict):
        user = self.context["request"].user
        return Artwork.objects.create(artist=user, **validated_data)
