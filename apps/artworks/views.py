from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.artworks.filters import ArtworkFilter
from apps.artworks.models import Artwork, StatusTextChoices
from apps.artworks.serializers import ArtworkListSerializer, ArtworkCreateSerializer


class ArtworkPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "limit"
    max_page_size = 75

    def get_paginated_response(self, data):
        return Response(
            {
                "data": data,
                "meta": {
                    "total": self.page.paginator.count,
                    "page": self.page.number,
                    "limit": self.get_page_size(self.request),
                    "totalPages": self.page.paginator.num_pages
                }
             }
        )


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkListSerializer
    pagination_class = ArtworkPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArtworkFilter

    def get_serializer_class(self):
        if self.action == "create":
            return ArtworkCreateSerializer
        return ArtworkListSerializer

    def get_queryset(self):
        queryset = Artwork.objects.select_related("artist").order_by("id")
        status = self.request.query_params.get("status")

        if not status:
            return queryset.filter(status=StatusTextChoices.APPROVED)

        return queryset
