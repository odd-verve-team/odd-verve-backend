from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.artworks.views import ArtworkViewSet

router = DefaultRouter()
router.register(r"", ArtworkViewSet, basename="artwork")

urlpatterns = [path("", include(router.urls))]
