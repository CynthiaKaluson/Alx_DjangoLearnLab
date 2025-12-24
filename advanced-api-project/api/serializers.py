"""
Custom serializers for the API application.
Handles complex data structures and nested relationships between Author and Book models.
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Serializes all fields of the Book model and includes custom validation
    to ensure the publication_year is not in the future.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Custom field validation to ensure publication year is not in the future.

        Args:
            value (int): The publication year to validate

        Returns:
            int: The validated publication year

        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested BookSerializer.

    Includes a nested representation of related books, allowing the API
    to return author details along with their books in a single response.
    The relationship is handled dynamically through the 'books' field
    which uses BookSerializer to serialize the related Book objects.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']