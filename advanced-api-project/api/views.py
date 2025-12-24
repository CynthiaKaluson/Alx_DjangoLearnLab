"""
Custom views and generic views for the API application.
Implements CRUD operations with custom behavior and permissions.
"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, BookDetailSerializer
from .permissions import IsAdminOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model providing CRUD operations.

    This ViewSet uses generic views internally to handle:
    - ListView: Retrieve all books
    - DetailView: Retrieve single book by ID
    - CreateView: Add new book
    - UpdateView: Modify existing book
    - DeleteView: Remove book

    Customizations:
    - Different serializers for list vs detail
    - Custom create/update methods
    - Permission-based access control
    """
    queryset = Book.objects.all().select_related('author')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['publication_year', 'genre', 'author']
    search_fields = ['title', 'isbn', 'author__name']
    ordering_fields = ['title', 'publication_year', 'price', 'pages']
    ordering = ['-publication_year']

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.

        Returns:
            BookDetailSerializer for retrieve actions
            BookSerializer for other actions
        """
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer

    def get_queryset(self):
        """
        Customize queryset based on request parameters.

        Returns:
            QuerySet: Filtered and optimized queryset
        """
        queryset = super().get_queryset()

        # Filter by price range if provided
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def perform_create(self, serializer):
        """
        Custom create method to add additional context.

        Args:
            serializer: BookSerializer instance
        """
        serializer.save()
        # Log creation (in a real app, you might use Django signals or logging)
        print(f"Book created: {serializer.instance.title}")

    def perform_update(self, serializer):
        """
        Custom update method.

        Args:
            serializer: BookSerializer instance
        """
        serializer.save()
        # Log update
        print(f"Book updated: {serializer.instance.title}")

    def perform_destroy(self, instance):
        """
        Custom destroy method.

        Args:
            instance: Book instance to delete
        """
        book_title = instance.title
        instance.delete()
        # Log deletion
        print(f"Book deleted: {book_title}")

    @action(detail=False, methods=['get'])
    def recent_books(self, request):
        """
        Custom action to get books published in the last 5 years.

        Returns:
            Response: List of recent books
        """
        from datetime import datetime
        current_year = datetime.now().year
        recent_books = self.get_queryset().filter(
            publication_year__gte=current_year - 5
        )

        page = self.paginate_queryset(recent_books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_price(self, request, pk=None):
        """
        Custom action to update book price.

        Args:
            request: HTTP request with new price
            pk: Primary key of the book

        Returns:
            Response: Updated book data or error
        """
        book = self.get_object()
        new_price = request.data.get('price')

        if new_price is None:
            return Response(
                {'error': 'Price is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            new_price = float(new_price)
            if new_price <= 0:
                return Response(
                    {'error': 'Price must be greater than zero'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {'error': 'Price must be a valid number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        book.price = new_price
        book.save()

        serializer = self.get_serializer(book)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Author model providing CRUD operations.

    This ViewSet handles author management with nested book information.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'birth_date']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """
        Custom action to get all books by a specific author.

        Args:
            request: HTTP request
            pk: Primary key of the author

        Returns:
            Response: List of books by the author
        """
        author = self.get_object()
        books = author.books.all()

        page = self.paginate_queryset(books)
        if page is not None:
            serializer = BookSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


# Traditional generic class-based views (alternative to ViewSet)
class BookListView(generics.ListAPIView):
    """
    Generic ListView for books (alternative to ViewSet).

    URL: GET /api/books-list/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['publication_year', 'genre', 'author']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'price']


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for single book (alternative to ViewSet).

    URL: GET /api/books/<id>/
    """
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class BookCreateView(generics.CreateAPIView):
    """
    Generic CreateView for books with custom permissions.

    URL: POST /api/books/create/
    Only authenticated users can create books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Custom create with additional logic."""
        serializer.save()
        # Additional logic here (e.g., send notifications)


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView for books.

    URL: PUT/PATCH /api/books/<id>/update/
    Only authenticated users can update books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """Custom update with additional logic."""
        serializer.save()
        # Additional logic here


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView for books.

    URL: DELETE /api/books/<id>/delete/
    Only admin users can delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_destroy(self, instance):
        """Custom destroy with additional logic."""
        book_title = instance.title
        super().perform_destroy(instance)
        # Additional logic here (e.g., logging, cleanup)