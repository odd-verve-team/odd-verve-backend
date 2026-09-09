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


class StatusTextChoices(models.TextChoices):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SOLD = "sold"


class MediumTextChoices(models.TextChoices):
    OIL = "oil"
    ACRYLIC = "acrylic"
    WATERCOLOR = "watercolor"
    GRAPHICS = "graphics"
    MIXED_MEDIA = "mixed_media"
    LITHOGRAPHY = "lithography"


class Artwork(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    category = models.CharField(max_length=30, choices=CategoryTextChoices.choices)
    painting_length = models.PositiveIntegerField()
    painting_width = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=30, choices=StatusTextChoices.choices, default=StatusTextChoices.PENDING)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    year = models.PositiveIntegerField()
    medium = models.CharField(max_length=30, choices=MediumTextChoices.choices)
    image_url = models.ImageField(
        upload_to="artworks_images/",
        width_field="image_width",
        height_field="image_height",
    )
    image_width = models.PositiveIntegerField(null=True, blank=True)
    image_height = models.PositiveIntegerField(null=True, blank=True)
