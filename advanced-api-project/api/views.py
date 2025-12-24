from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# ListView: Retrieve all books
class BookListView(generics.ListAPIView):
    """
    API view to retrieve list of books.
    Accessible to all users (authenticated and unauthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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