from django.urls import path

from apps.favorites.views import (
    FavoriteListView,
    FavoriteCreateView,
    FavoriteDeleteView,
)

urlpatterns = [
    path("", FavoriteListView.as_view(), name="favorites"),
    path("", FavoriteCreateView.as_view(), name="create_favorite"),
    path("<int:pk>/", FavoriteDeleteView.as_view(), name="delete_favorite"),
]
