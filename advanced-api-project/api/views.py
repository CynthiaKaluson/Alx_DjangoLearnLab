from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Book


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