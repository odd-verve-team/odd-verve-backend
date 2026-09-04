from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import viewsets

from apps.artworks.models import Artwork, StatusTextChoices
from apps.artworks.serializers import ArtworkListSerializer, ArtworkCreateSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Get list of artworks",
        description="Returns list of all artworks with "
                    "filtering option by 'is_featured' field",
        parameters=[
            OpenApiParameter(
                name="is_featured",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter featured artworks using query params: ?is_featured=true",
                required=False,
            ),
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                enum=StatusTextChoices.values,
                description="Filter artworks with status using query params: ?status=published",
                required=False,
            ),
        ],
        responses={200: ArtworkListSerializer(many=True)},
    )
)
class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ArtworkCreateSerializer
        return ArtworkListSerializer

    def get_queryset(self):
        queryset = Artwork.objects.all().select_related("artist")

        is_featured = self.request.query_params.get("is_featured")
        if is_featured:
            is_featured = is_featured.lower()
        status = self.request.query_params.get("status")

        if is_featured == "true":
            queryset = queryset.filter(is_featured=True)
        if is_featured == "false":
            queryset = queryset.filter(is_featured=False)
        if status:
            queryset = queryset.filter(status=status.lower())
        return queryset
