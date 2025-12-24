# api/filters.py
"""
Custom filters for the API application.
Provides filtering, searching, and ordering capabilities for Book model.
"""
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    """
    FilterSet for Book model with advanced filtering options.

    Allows users to filter books by:
    - title (exact match or contains)
    - author (exact match or contains)
    - publication_year (exact, range)
    """

    # Title filtering
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text="Filter by title (case-insensitive contains)"
    )

    title_exact = django_filters.CharFilter(
        field_name='title',
        lookup_expr='exact',
        help_text="Filter by exact title match"
    )

    # Author filtering (CharField, not ForeignKey)
    author = django_filters.CharFilter(
        field_name='author',
        lookup_expr='icontains',
        help_text="Filter by author name (case-insensitive contains)"
    )

    author_exact = django_filters.CharFilter(
        field_name='author',
        lookup_expr='exact',
        help_text="Filter by exact author name"
    )

    # Publication year filtering
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        help_text="Filter by exact publication year"
    )

    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text="Filter by minimum publication year"
    )

    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text="Filter by maximum publication year"
    )

    # Search across multiple fields
    search = django_filters.CharFilter(
        method='custom_search',
        help_text="Search across title and author fields"
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def custom_search(self, queryset, name, value):
        """
        Custom search method that searches across title and author.

        Args:
            queryset: The original queryset
            name: The field name ('search')
            value: The search term

        Returns:
            Filtered queryset with books matching search term
        """
        if value:
            return queryset.filter(
                title__icontains=value
            ) | queryset.filter(
                author__icontains=value
            )
        return queryset