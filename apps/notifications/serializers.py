from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Notification
from ..users.models import Profile, RoleTextChoices


class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "created_at", "title", "message_body")


class NotificationBuyArtworkSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.IntegerField(allow_null=True)
    country_or_city = serializers.CharField(max_length=255, allow_null=True)
    message = serializers.CharField(max_length=2000, allow_null=True)
    artwork = serializers.PrimaryKeyRelatedField()

    def create(self, validated_data):
        artwork = validated_data["artwork"]
        user_message = validated_data["message"]
        full_name = validated_data["full_name"]
        first_name, last_name = full_name.split(" ")
        author_profile = artwork.profile.id
        notification_body = (
            f"User {first_name} {last_name} wants to buy your artwork {artwork.title}."
        )
        if user_message:
            notification_body = f"{notification_body} User's message: {user_message}."
        return Notification.objects.create(
            profile=author_profile,
            title=f"Purchase notification",
            message_body=notification_body,
            **validated_data,
        )

    def validate_full_name(self, value):
        if value.split(" ") > 3 or value.split(" ") == 1:
            raise ValidationError(detail="Invalid full name")

    def validate_phone_number(self, value):
        if value < 15:
            raise ValidationError(
                detail="Phone number can not have more than 15 symbols"
            )


class NotificationBecomeArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ()

    @transaction.atomic
    def create(self, validated_data):
        admin_profiles = [
            Profile.objects.filter(user__role=RoleTextChoices.ADMIN).select_related(
                "user"
            )
        ]
        user = self.context["request"].user
        notifications = [
            Notification(
                profile=profile,
                title="Artist notification",
                message_body=f"User (id: {user.id}) {user.first_name} {user.last_name} wants to become an artist. Check his profile is it valid to be an artist.",
            )
            for profile in admin_profiles
        ]
        return Notification.objects.bulk_create(notifications)
