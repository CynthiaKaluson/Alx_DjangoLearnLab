from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from .models import Book
from .serializers import BookSerializer


# ListView: Retrieve all books with filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    """
    API view to retrieve list of books.
    Supports filtering by title, author, and publication_year.
    Supports searching by title and author.
    Supports ordering by title and publication_year.
    Accessible to all users (authenticated and unauthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, and ordering
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering: Allow filtering by title, author, and publication_year
    filterset_fields = ['title', 'author', 'publication_year']

    # Searching: Allow searching by title and author
    search_fields = ['title', 'author']

    # Ordering: Allow ordering by title and publication_year
    ordering_fields = ['title', 'publication_year']

    # Default ordering
    ordering = ['title']


# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by ID.
    Accessible to all users (authenticated and unauthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# CreateView: Add a new book
class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    Only accessible to authenticated users.
    Handles form submissions and data validation automatically.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    Only accessible to authenticated users.
    Handles form submissions and data validation automatically.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    Only accessible to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]