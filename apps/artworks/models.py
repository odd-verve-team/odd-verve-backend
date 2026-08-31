from django.db import models

from apps.users.models import User


class CategoryTextChoices(models.TextChoices):
    MODERN = "modern"
    PORTRAIT = "portrait"
    ABSTRACTIONISM = "abstractionism"
    CUBISM = "cubism"
    SURREALISM = "surrealism"
    POP_ART = "pop art"
    IMPRESSIONISM = "impressionism"
    LANDSCAPE = "landscape"
    STILL_LIFE = "still_life"
    ROMANTICISM = "romanticism"


class ModerationStatusTextChoices(models.TextChoices):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class StatusTextChoices(models.TextChoices):
    DRAFT = "draft"
    PUBLISHED = "published"
    SOLD = "sold"
    RESERVED = "reserved"


class Artwork(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    category = models.CharField(max_length=30, choices=CategoryTextChoices.choices)
    length = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    moderation_status = models.CharField(
        max_length=30, choices=ModerationStatusTextChoices.choices
    )
    status = models.CharField(max_length=30, choices=StatusTextChoices.choices)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    image_url = models.URLField()
