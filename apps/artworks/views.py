import re

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.artworks.filters import ArtworkFilter
from apps.artworks.models import Artwork, StatusTextChoices
from apps.artworks.serializers import (
    ArtworkListSerializer,
    ArtworkDetailSerializer,
    ArtworkSearchSerializer,
)


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
                    "totalPages": self.page.paginator.num_pages,
                },
            }
        )


class ArtworkListView(generics.ListAPIView):
    serializer_class = ArtworkListSerializer
    pagination_class = ArtworkPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArtworkFilter

    def get_queryset(self):
        queryset = Artwork.objects.select_related("profile").order_by("id")
        status = self.request.query_params.get("status")

        if not status:
            return queryset.filter(status=StatusTextChoices.APPROVED)

        return queryset


class ArtworkDetailView(generics.RetrieveAPIView):
    queryset = Artwork.objects.select_related("profile").all()
    serializer_class = ArtworkDetailSerializer


class ArtworkSearchView(generics.ListAPIView):
    serializer_class = ArtworkSearchSerializer

    def list(self, request, *args, **kwargs):
        text = request.query_params.get("text")
        if text and bool(re.search(r"[a-zA-Z]", text)):
            text = re.sub(r"[^a-zA-Z]", "", text)
            queryset = Artwork.objects.filter(title__icontains=text)[:4]
            serializer = ArtworkSearchSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return []
