"""
Custom filters for the API application.
"""
import django_filters
from django.db.models import Q
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Custom filter set for Book model.

    Provides advanced filtering options beyond simple field lookups.
    """
    # Range filters for numeric fields
    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        label='Minimum publication year'
    )
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        label='Maximum publication year'
    )

    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Minimum price'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Maximum price'
    )

    pages_min = django_filters.NumberFilter(
        field_name='pages',
        lookup_expr='gte',
        label='Minimum pages'
    )
    pages_max = django_filters.NumberFilter(
        field_name='pages',
        lookup_expr='lte',
        label='Maximum pages'
    )

    # Choice-based filter with custom options
    genre = django_filters.ChoiceFilter(
        choices=Book.GENRE_CHOICES,
        label='Genre'
    )

    # Author name filter (search across related model)
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        label='Author name contains'
    )

    # Multiple choice filter
    genres = django_filters.BaseInFilter(
        field_name='genre',
        lookup_expr='in',
        label='Multiple genres'
    )

    # Boolean filter for recent books
    recent = django_filters.BooleanFilter(
        method='filter_recent',
        label='Published in last 5 years'
    )

    # Custom search across multiple fields
    search = django_filters.CharFilter(
        method='custom_search',
        label='Search in title and author name'
    )

    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'publication_year': ['exact'],
            'author': ['exact'],
            'isbn': ['exact'],
        }

    def filter_recent(self, queryset, name, value):
        """
        Custom filter method for recent books.

        Args:
            queryset: Original queryset
            name: Field name
            value: Boolean value

        Returns:
            Filtered queryset
        """
        from datetime import datetime
        current_year = datetime.now().year

        if value:
            return queryset.filter(publication_year__gte=current_year - 5)
        return queryset.filter(publication_year__lt=current_year - 5)

    def custom_search(self, queryset, name, value):
        """
        Custom search across multiple fields.

        Args:
            queryset: Original queryset
            name: Field name
            value: Search term

        Returns:
            Filtered queryset
        """
        if value:
            return queryset.filter(
                Q(title__icontains=value) |
                Q(author__name__icontains=value) |
                Q(isbn__icontains=value)
            )
        return queryset


class AuthorFilter(django_filters.FilterSet):
    """
    Custom filter set for Author model.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    has_books = django_filters.BooleanFilter(
        method='filter_has_books',
        label='Has published books'
    )

    # Date range filter
    birth_date_after = django_filters.DateFilter(
        field_name='birth_date',
        lookup_expr='gte',
        label='Born after'
    )
    birth_date_before = django_filters.DateFilter(
        field_name='birth_date',
        lookup_expr='lte',
        label='Born before'
    )

    class Meta:
        model = Author
        fields = ['name']

    def filter_has_books(self, queryset, name, value):
        """
        Filter authors based on whether they have published books.

        Args:
            queryset: Original queryset
            name: Field name
            value: Boolean value

        Returns:
            Filtered queryset
        """
        if value:
            return queryset.filter(books__isnull=False).distinct()
        return queryset.filter(books__isnull=True)