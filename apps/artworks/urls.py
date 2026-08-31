from django.urls import path

from apps.artworks.views import ArtworkListView

urlpatterns = [
    path("", ArtworkListView.as_view(), name="artworks")
]

app_name = "artworks"
