from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book


class BookAPITestCase(TestCase):
    """
    Test suite for Book API endpoints.
    Tests CRUD operations, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        """
        Set up test client, test user, and sample book data.
        Runs before each test method.
        """
        # Create API client
        self.client = APIClient()

        # Create test user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create sample books for testing
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            author='William Vincent',
            publication_year=2023
        )

        self.book2 = Book.objects.create(
            title='Python Crash Course',
            author='Eric Matthes',
            publication_year=2019
        )

        self.book3 = Book.objects.create(
            title='Django REST Framework Guide',
            author='William Vincent',
            publication_year=2024
        )

    def test_list_books(self):
        """
        Test retrieving list of all books.
        Should return 200 OK and list of books.
        """
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book_detail(self):
        """
        Test retrieving a single book by ID.
        Should return 200 OK and book details.
        """
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')
        self.assertEqual(response.data['author'], 'William Vincent')

    def test_create_book_authenticated(self):
        """
        Test creating a new book with authentication.
        Should return 201 CREATED and book data.
        """
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2025
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'New Book')

    def test_create_book_unauthenticated(self):
        """
        Test creating a book without authentication.
        Should return 403 FORBIDDEN.
        """
        data = {
            'title': 'Unauthorized Book',
            'author': 'Unauthorized Author',
            'publication_year': 2025
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication.
        Should return 200 OK and updated data.
        """
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Updated Django Book',
            'author': 'William Vincent',
            'publication_year': 2023
        }
        response = self.client.put(f'/api/books/update/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Django Book')

    def test_update_book_unauthenticated(self):
        """
        Test updating a book without authentication.
        Should return 403 FORBIDDEN.
        """
        data = {
            'title': 'Unauthorized Update',
            'author': 'William Vincent',
            'publication_year': 2023
        }
        response = self.client.put(f'/api/books/update/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication.
        Should return 204 NO CONTENT and remove book from database.
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_book_unauthenticated(self):
        """
        Test deleting a book without authentication.
        Should return 403 FORBIDDEN.
        """
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_author(self):
        """
        Test filtering books by author.
        Should return only books by specified author.
        """
        response = self.client.get('/api/books/?author=William Vincent')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for book in response.data:
            self.assertEqual(book['author'], 'William Vincent')

    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        Should return only books from specified year.
        """
        response = self.client.get('/api/books/?publication_year=2023')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2023)

    def test_search_books(self):
        """
        Test searching books by title or author.
        Should return books matching search query.
        """
        response = self.client.get('/api/books/?search=Django')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_order_books_by_title(self):
        """
        Test ordering books by title (ascending).
        Should return books sorted alphabetically by title.
        """
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year (descending).
        Should return books sorted by year from newest to oldest.
        """
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering.
        Should apply all parameters correctly.
        """
        response = self.client.get(
            '/api/books/?author=William Vincent&search=Django&ordering=publication_year'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_invalid_book_creation_missing_fields(self):
        """
        Test creating a book with missing required fields.
        Should return 400 BAD REQUEST.
        """
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Incomplete Book'
            # Missing author and publication_year
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        Should return 404 NOT FOUND.
        """
        response = self.client.get('/api/books/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)