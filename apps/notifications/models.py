from django.db import models

from apps.artworks.models import Artwork
from apps.users.models import Profile


class Notification(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        related_name="notifications",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    profile = models.ForeignKey(
        Profile, related_name="notifications", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    message_body = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
