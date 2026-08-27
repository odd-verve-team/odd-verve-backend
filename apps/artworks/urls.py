from django.urls import path
from .views import ArtworkListView

urlpatterns = [
    path('', ArtworkListView.as_view()),
]