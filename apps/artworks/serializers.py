from rest_framework import serializers

from apps.artworks.models import Artwork


class ArtworkListSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Artwork
        fields = ("image_url", "author_full_name")

    def get_author_full_name(self, obj):
        full_name = f"{obj.artist.name} {obj.arist.surname}"
        full_name = full_name.title()
        return f"{obj.artist.username}\n{full_name}"


class ArtworkCreateSerializer(serializers.ModelSerializer):
    image_field = serializers.ImageField(required=True)

    class Meta:
        model = Artwork
        fields = "__all__"
