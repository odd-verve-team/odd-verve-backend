from typing import Any, Optional
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import AuthUser
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token, RefreshToken


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
            self.email: attrs[self.email],
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
        return cls.token_class.for_user(user)  # type: ignore


class CustomTokenObtainSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email",)


class UserListSerializer(serializers.ModelSerializer):
    artworks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    art_categories = serializers.SerializerMethodField()

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

    def get_art_categories(self, obj):
        unique_categories = []
        artworks = obj.artworks.all()
        for artwork in artworks:
            if artwork.category not in unique_categories:
                unique_categories.append(artwork.category)
        return unique_categories


class UserDetailSerializer(UserListSerializer):
    class Meta(UserListSerializer.Meta):
        model = get_user_model()
        fields = UserListSerializer.Meta.fields + (
            "application_status",
            "number_of_paid_cell",
            "created_at",
            "bio",
        )
