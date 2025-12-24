from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Handles serialization and deserialization of Book instances.
    """
    class Meta:
        model = Book
        fields = '__all__'