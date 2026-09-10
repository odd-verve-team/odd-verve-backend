import django_filters
from django.db.models import F

from apps.artworks.models import (
    Artwork,
    StatusTextChoices,
    CategoryTextChoices,
    MediumTextChoices,
)


class ChoiceInFilter(django_filters.BaseInFilter, django_filters.ChoiceFilter):
    pass


class ArtworkFilter(django_filters.FilterSet):
    is_featured = django_filters.BooleanFilter()
    status = django_filters.ChoiceFilter(choices=StatusTextChoices.choices)
    price_lte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    year_lte = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    category = ChoiceInFilter(lookup_expr="in", choices=CategoryTextChoices.choices)
    medium = ChoiceInFilter(lookup_expr="in", choices=MediumTextChoices.choices)
    size = django_filters.CharFilter(method="filter_by_size")

    sort = django_filters.CharFilter(method="filter_by_sort")

    def filter_by_size(self, queryset, name, value):
        try:
            value = value.split(",")
            for size in value:
                painting_length, painting_width = size.split("x")
                painting_length, painting_width = (
                    painting_length.strip(),
                    painting_width.strip(),
                )
                if painting_length.isdigit() and painting_width.isdigit():
                    return queryset.filter(
                        painting_length=painting_length, painting_width=painting_width
                    )
            return queryset
        except Exception:
            return queryset

    def filter_by_sort(self, queryset, name, value):
        mapping = {
            "price_asc": "price",
            "price_desc": "-price",
            "date_asc": "created_at",
            "date_desc": "-created_at",
            "year_asc": "year",
            "year_desc": "-year",
            "size_asc": "size",
            "size_desc": "-size",
        }

        order_fields = value.split(",")

        order_list = []
        for field in order_fields:
            mapped_field = mapping.get(field.strip())
            if mapped_field in ("size", "-size"):
                queryset = queryset.annotate(
                    size=F("painting_length") * F("painting_width")
                )
                order_list.append(mapped_field)
            elif mapped_field:
                order_list.append(mapped_field)

        queryset = queryset.order_by(*order_list)

        return queryset

    class Meta:
        model = Artwork
        fields = (
            "is_featured",
            "status",
            "price_lte",
            "year_lte",
            "category",
            "medium",
            "size",
            "sort",
        )
