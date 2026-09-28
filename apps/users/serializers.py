from typing import Any, Optional
from apps.users.backends import CustomBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
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

        custom_backend = CustomBackend()

        self.user = custom_backend.authenticate(**authenticate_kwargs)

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
