import csv
import os
import time

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from google import genai
from google.genai import types
from apps.rag.models import Document

load_dotenv()


class Command(BaseCommand):
    help = "converts documents into vectors and saves them in db"

    def handle(self, *args, **options):

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        def convert_text_to_embedding(text: str) -> list[float]:
            try:
                result = client.models.embed_content(
                    model="gemini-embedding-001",
                    contents=text,
                    config=types.EmbedContentConfig(
                        task_type="RETRIEVAL_DOCUMENT",
                        output_dimensionality=768,
                    ),
                )
                return result.embeddings[0].values
            except Exception as e:
                raise ValueError(f"error: {e}")

        def create_vector_document_in_db(title: str, body: str) -> None:
            embedding = convert_text_to_embedding(f"{title}\n\n{body}")
            Document.objects.create(title=title, body=body, embedding=embedding)

        with open("documents.csv", "r", encoding="utf-8-sig") as file:
            documents = csv.DictReader(file)
            for document in documents:
                try:
                    time.sleep(30)
                    create_vector_document_in_db(
                        title=document["title"], body=document["body"]
                    )
                    print(f"{document} vector created in db")
                except Exception as e:
                    print(f"Error {e}")
                    continue

        self.stdout.write(self.style.SUCCESS("Created vectors"))
