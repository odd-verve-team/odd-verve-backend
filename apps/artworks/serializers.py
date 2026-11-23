from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.artworks.models import Artwork


class ArtistSerializer(serializers.ModelSerializer):
    first_name = serializers.SlugRelatedField(
        many=False, slug_field="first_name", source="artist_profile", read_only=True
    )
    last_name = serializers.SlugRelatedField(
        many=False, slug_field="last_name", source="artist_profile", read_only=True
    )
    avatar_url = serializers.SlugRelatedField(
        many=False, slug_field="avatar_url", source="artist_profile", read_only=True
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


class ArtworkDetailSerializer(serializers.ModelSerializer):
    art_categories = serializers.SlugRelatedField(
        slug_field="category",
        many=True,
        source="profile",
        read_only=True,
    )
    bio = serializers.SlugRelatedField(
        slug_field="bio",
        many=False,
        source="profile",
        read_only=True,
    )
    artist = ArtistSerializer.Meta.fields + ("art_categories", "bio")

    class Meta:
        model = Artwork
        fields = (
            "id",
            "artist",
            "title",
            "description",
            "category",
            "painting_length",
            "painting_width",
            "price",
            "status",
            "is_featured",
            "year",
            "medium",
            "image_url",
            "image_width",
            "image_height",
        )
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
