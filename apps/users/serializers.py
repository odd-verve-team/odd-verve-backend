from typing import Any, Optional
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from email_validator import validate_email, EmailNotValidError
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import AuthUser
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token, RefreshToken

from apps.users.models import ArtistProfile


class TokenObtainSerializer(serializers.Serializer):
    email = get_user_model().EMAIL_FIELD
    token_class: Optional[type[Token]] = None

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields[self.email] = serializers.EmailField(write_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        authenticate_kwargs = {
            "email": attrs[self.email],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            raise ValidationError(detail="User not found or email is invalid")

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        return {}

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        return cls.token_class.for_user(user)


class CustomTokenObtainSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh_token"] = str(refresh)
        data["access_token"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email",)

    def create(self, validated_data):
        return get_user_model().objects.create(**validated_data)

    def validate_email(self, value):
        try:
            validate_email(value, check_deliverability=True)
        except EmailNotValidError as e:
            raise ValidationError(detail=f"Email is incorrect: {e}")
        return value


class ArtistSerializer(serializers.ModelSerializer):
    artworks = serializers.PrimaryKeyRelatedField(many=True)
    art_categories = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "role",
            "application_status",
            "artworks",
            "art_categories",
        )

    def get_art_categories(self, obj):
        unique_categories = []
        artworks = obj.artworks.all()
        for artwork in artworks:
            if artwork.category not in unique_categories:
                unique_categories.append(artwork.category)
        return unique_categories


class ArtistProfileListSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()

    class Meta:
        model = ArtistProfile
        fields = (
            "id",
            "artist",
            "username",
            "first_name",
            "last_name",
            "avatar_url",
        )


class ArtistProfileDetailSerializer(ArtistProfileListSerializer):
    class Meta(ArtistProfileListSerializer.Meta):
        model = ArtistProfile
        fields = ArtistProfileListSerializer.Meta.fields + (
            "number_of_paid_cell" "phone_number",
            "created_at",
            "bio",
            "statement",
            "style",
            "address",
            "social_media",
        )
