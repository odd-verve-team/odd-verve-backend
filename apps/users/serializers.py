from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.artworks.models import Artwork
from apps.users.security import validate_password_complexity


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value: str) -> str:
        validation_message = validate_password_complexity(value)
        if validation_message:
            raise serializers.ValidationError(validation_message)
        return value

    def create(self, validated_data: dict):
        return get_user_model().objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="category",
        many=True,
        queryset=Artwork.objects.all()
    )
    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserDetailSerializer(UserListSerializer):
    pass
