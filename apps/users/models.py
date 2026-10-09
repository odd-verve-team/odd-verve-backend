from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


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
    email = models.EmailField()
    username = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    password = models.CharField(max_length=128, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True, unique=True)
    avatar_url = models.ImageField(
        upload_to="avatar_images/", default="default_avatar.png", blank=True
    )
    role = models.CharField(
        max_length=20, choices=RoleTextChoices.choices, default=RoleTextChoices.USER
    )
    application_status = models.CharField(
        max_length=20,
        choices=ApplicationStatusTextChoices.choices,
        null=True,
        blank=True,
    )
    statement = models.TextField(null=True, blank=True)
    style = models.TextField(null=True, blank=True)
    number_of_paid_cell = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=2000, null=True, blank=True)
    address = models.OneToOneField(
        "Address", on_delete=models.SET_NULL, blank=True, null=True, related_name="user"
    )
    social_media = models.OneToOneField("SocialMedia", on_delete=models.SET_NULL, blank=True, null=True, related_name="user")

    objects = UserManager()


class Address(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.PositiveIntegerField()


class SocialMedia(models.Model):
    instagram = models.URLField(max_length=255, unique=True)
    telegram = models.URLField(max_length=255, unique=True)
    twitter = models.URLField(max_length=255, unique=True)
    facebook = models.URLField(max_length=255, unique=True)
