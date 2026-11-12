from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email"""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, **extra_fields):
        """Create and save a regular User with the given email"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class RoleTextChoices(models.TextChoices):
    USER = "user"
    ARTIST = "artist"
    ADMIN = "admin"


class ApplicationStatusTextChoices(models.TextChoices):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email_address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    role = models.CharField(
        max_length=6, choices=RoleTextChoices.choices, default=RoleTextChoices.USER
    )
    application_status = models.CharField(
        max_length=8,
        choices=ApplicationStatusTextChoices.choices,
        null=True,
        blank=True,
    )

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.id} User"


class ArtistProfile(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="artist_profile"
    )
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    avatar_url = models.ImageField(
        upload_to="avatar_images/",
        default="default_avatar.png",
    )
    statement = models.TextField(max_length=200, unique=True, null=True, blank=True)
    style = models.TextField(max_length=200, unique=True, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.artist.id} User's profile"


class Address(models.Model):
    user = models.OneToOneField(
        ArtistProfile, on_delete=models.CASCADE, related_name="address"
    )
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)


class SocialMedia(models.Model):
    user = models.OneToOneField(
        ArtistProfile, on_delete=models.CASCADE, related_name="social_media"
    )
    instagram = models.URLField(unique=True, null=True, blank=True)
    telegram = models.URLField(unique=True, null=True, blank=True)
    twitter = models.URLField(unique=True, null=True, blank=True)
    facebook = models.URLField(unique=True, null=True, blank=True)
