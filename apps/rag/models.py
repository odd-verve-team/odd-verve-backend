from django.db import models
from pgvector.django import VectorField, HnswIndex


class Document(models.Model):
    title = models.CharField(max_length=50, unique=True)
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
