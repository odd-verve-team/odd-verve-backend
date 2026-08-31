from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.artworks.views import ArtworkViewSet


router = DefaultRouter()
router.register("artworks", ArtworkViewSet)


urlpatterns = [
    path("", include(router.urls))
]

app_name = "artworks"
