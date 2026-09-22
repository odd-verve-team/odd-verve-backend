from django.urls import path

from apps.rag.views import ai

urlpatterns = [
    path("chat/", ai)
]

app_name = "ai"
