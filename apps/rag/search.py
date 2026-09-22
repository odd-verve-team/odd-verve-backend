import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pgvector.django import CosineDistance

from apps.rag.models import Document

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_embedding(text: str) -> list[float]:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768,
        )
    )
    return result.embeddings[0].values


def search(query: str, top_k: int = 3) -> list[dict]:
    query_embedding = get_embedding(query)
    documents = (
        Document.objects.annotate(
            distance=CosineDistance("embedding", query_embedding)
        )
    ).order_by("distance")[:top_k]

    return [
        {
            "title": doc.title,
            "body": doc.body,
            "similarity": round(1 - doc.distance, 4)
        }
        for doc in documents
    ]
