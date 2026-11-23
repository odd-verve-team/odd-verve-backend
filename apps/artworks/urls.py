from django.urls import path

from apps.artworks.views import ArtworkListView, ArtworkDetailView, ArtworkSearchView

urlpatterns = [
    path(
        "",
        ArtworkListView.as_view(),
    ),
    path("<int:pk>/", ArtworkDetailView.as_view()),
    path("search/", ArtworkSearchView.as_view()),
]
