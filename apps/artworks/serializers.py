from rest_framework import serializers
from apps.artworks.models import Artwork


class ArtworkListSerializer(serializers.ModelSerializer):
    artist_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Artwork
        fields = "__all__"
        read_only_fields = ("image_width", "image_height")

    def get_artist_full_name(self, obj):
        full_name = f"{obj.artist.first_name} {obj.artist.last_name}"
        full_name = full_name.title()
        return f"{obj.artist.username} {full_name}"


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
            "image_url",
        )

    def create(self, validated_data: dict):
        user = self.context["request"].user
        return Artwork.objects.create(artist=user, **validated_data)
