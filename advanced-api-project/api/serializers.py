# api/serializers.py
"""
Custom serializers for the API application.
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Serializes all fields of the Book model and includes custom validation
    to ensure the publication_year is not in the future.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']

    def validate_publication_year(self, value):
        """
        Custom field validation to ensure publication year is not in the future.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value