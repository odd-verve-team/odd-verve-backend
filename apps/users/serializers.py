from django.contrib.auth import get_user_model
from rest_framework import serializers
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
    artworks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    art_categories = serializers.SlugRelatedField(
        slug_field="category", many=True, read_only=True, source="artworks"
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar_url",
            "role",
            "artworks",
            "art_categories",
        )


class UserDetailSerializer(UserListSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar_url",
            "role",
            "application_status",
            "number_of_paid_cell",
            "artworks",
            "art_categories",
            "created_at",
            "bio",
        )
