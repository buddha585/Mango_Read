from django_filters.rest_framework import ModelMultipleChoiceFilter, FilterSet, RangeFilter
from manga.models import Manga, Type, Genre


class MangaFilter(FilterSet):
    """Manga filtering"""
    type = ModelMultipleChoiceFilter(queryset=Type.objects.all())
    release_year = RangeFilter()
    genre = ModelMultipleChoiceFilter(queryset=Genre.objects.all())

    class Meta:
        model = Manga
        fields = ["release_year", "type", "genre"]