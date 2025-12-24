"""
Custom views and generic views for the API application.
Implements CRUD operations for Book model with custom behavior and permissions.
"""
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all books.

    URL: GET /api/books/
    Allows read-only access to all users (authenticated or not).
    Returns a list of all books in the database.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view books

    def get_queryset(self):
        """
        Customize the queryset if needed.
        Can be extended for filtering or additional logic.
        """
        return Book.objects.all().select_related('author')


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single book by ID.

    URL: GET /api/books/<int:pk>/
    Allows read-only access to all users (authenticated or not).
    Returns detailed information about a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'  # Default is 'pk', explicitly stated for clarity


class BookCreateView(generics.CreateAPIView):
    """
    Generic CreateView for adding a new book.

    URL: POST /api/books/create/
    Restricts access to authenticated users only.
    Validates data using BookSerializer's validation rules.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in

    def perform_create(self, serializer):
        """
        Customize the creation process.
        Called after validation but before saving.

        Args:
            serializer: Validated BookSerializer instance
        """
        serializer.save()
        # Additional logic can be added here (e.g., logging, notifications)


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView for modifying an existing book.

    URL: PUT/PATCH /api/books/<int:pk>/update/
    Restricts access to authenticated users only.
    PUT for full updates, PATCH for partial updates.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """
        Customize the update process.

        Args:
            serializer: Validated BookSerializer instance
        """
        serializer.save()
        # Additional logic can be added here


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView for removing a book.

    URL: DELETE /api/books/<int:pk>/delete/
    Restricts access to authenticated users only.
    Permanently removes the book from the database.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        """
        Customize the deletion process.

        Args:
            instance: Book instance to be deleted
        """
        # Additional logic before deletion (e.g., logging, cleanup)
        instance.delete()


# Bonus: Views for Author model (optional but useful)
class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors with their books.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author with their books.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'