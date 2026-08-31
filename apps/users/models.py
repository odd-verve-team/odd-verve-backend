from django.contrib.auth.models import AbstractUser
from django.db import models


class RoleTextChoices(models.TextChoices):
    USER = "user"
    ARTIST = "artist"
    ADMIN = "admin"


class ApplicationStatusTextChoices(models.TextChoices):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class User(AbstractUser):
    avatar_url = models.URLField()
    role = models.CharField(max_length=20, choices=RoleTextChoices.choices)
    application_status = models.CharField(
        max_length=20,
        choices=ApplicationStatusTextChoices.choices,
        null=True,
        blank=True,
    )
    number_of_paid_cell = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=2000)
