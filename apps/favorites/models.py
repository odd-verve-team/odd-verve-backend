from django.db import models

from apps.artworks.models import Artwork
from apps.users.models import Profile


class Favorite(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="favorites"
    )
    artwork = models.ForeignKey(
        Artwork, on_delete=models.CASCADE, related_name="favorites"
    )
