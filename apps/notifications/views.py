from rest_framework import generics

from core.tasks.emails import send_email
from .models import Notification
from .serializers import (
    NotificationListSerializer,
    NotificationBuyArtworkSerializer,
    NotificationBecomeArtistSerializer,
)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationListSerializer

    def get_queryset(self):
        return (
            Notification.objects.filter(profile=self.request.user.profile.id)
            .select_related("artwork", "profile")
            .all()
        )


class NotificationBuyArtworkView(generics.CreateAPIView):
    serializer_class = NotificationBuyArtworkSerializer
    queryset = Notification.objects.select_related("artwork", "profile").all()

    def perform_create(self, serializer) -> None:
        artwork = serializer.data["artwork"]
        user_message = serializer.data["message"]
        author_email = artwork.profile.user.email
        user = self.request.user
        notification_body = f"User {user.first_name} {user.last_name} wants to buy your artwork {artwork.title}."
        if user_message:
            notification_body = f"{notification_body} User's message: {user_message}."
        send_email(
            email_title="Purchase notification",
            email_body=notification_body,
            receiver_email=author_email,
        )


class NotificationBecomeArtistView(generics.CreateAPIView):
    serializer_class = NotificationBecomeArtistSerializer
    queryset = Notification.objects.select_related("artwork", "profile").all()
