from django.urls import path

from apps.users.views.artist_views import ArtistProfileListView, ArtistProfileDetailView

urlpatterns = [
    path("profiles/", ArtistProfileListView.as_view(), name="artist_profiles"),
    path(
        "profiles/<int:pk>/",
        ArtistProfileDetailView.as_view(),
        name="artist_detail_profile",
    ),
]

app_name = "users"
