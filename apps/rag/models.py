from django.db import models
from pgvector.django import VectorField, HnswIndex

from apps.users.models import User


class ChatRolesTextChoices(models.TextChoices):
    USER = "user"
    MODEL = "model"


class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="message")
    role = models.CharField(max_length=255, choices=ChatRolesTextChoices.choices)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField()
    embedding = VectorField(dimensions=768)

    class Meta:
        indexes = [
            HnswIndex(
                name="docs_embedding_hnsw_index",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"]
            )
        ]

    def __str__(self) -> str:
        return self.title
