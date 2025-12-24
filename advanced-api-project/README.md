# Advanced API Project - Book Management API

## Overview
This project implements a RESTful API for managing books using Django REST Framework with advanced query capabilities including filtering, searching, and ordering.

## API Endpoints

### Public Endpoints (Read-Only Access)
- `GET /api/books/` - List all books (supports filtering, searching, and ordering)
- `GET /api/books/<int:pk>/` - Retrieve a single book by ID

### Protected Endpoints (Authentication Required)
- `POST /api/books/create/` - Create a new book
- `PUT /api/books/update/<int:pk>/` - Update an existing book
- `DELETE /api/books/delete/<int:pk>/` - Delete a book

## Advanced Query Capabilities

### 1. Filtering
Filter books by specific field values.

**Available Filter Fields:**
- `title` - Exact match on book title
- `author` - Exact match on author name
- `publication_year` - Exact match on publication year

**Examples:**
```bash
# Filter by title
GET /api/books/?title=Django%20for%20Beginners

# Filter by author
GET /api/books/?author=William%20Vincent

# Filter by publication year
GET /api/books/?publication_year=2023

# Combine multiple filters
GET /api/books/?author=William%20Vincent&publication_year=2023
```

**Using curl:**
```bash
curl "http://localhost:8000/api/books/?author=William%20Vincent"
```

### 2. Searching
Search for books using partial text matching.

**Available Search Fields:**
- `title` - Partial match on book title
- `author` - Partial match on author name

**Examples:**
```bash
# Search for books with "Django" in title or author
GET /api/books/?search=Django

# Search for books with "Python" in title or author
GET /api/books/?search=Python
```

**Using curl:**
```bash
curl "http://localhost:8000/api/books/?search=Django"
```

### 3. Ordering
Sort books by specific fields in ascending or descending order.

**Available Ordering Fields:**
- `title` - Sort by book title
- `publication_year` - Sort by publication year

**Examples:**
```bash
# Order by title (ascending - default)
GET /api/books/?ordering=title

# Order by title (descending)
GET /api/books/?ordering=-title

# Order by publication year (ascending)
GET /api/books/?ordering=publication_year

# Order by publication year (descending)
GET /api/books/?ordering=-publication_year
```

**Using curl:**
```bash
# Ascending order
curl "http://localhost:8000/api/books/?ordering=publication_year"

# Descending order (note the minus sign)
curl "http://localhost:8000/api/books/?ordering=-publication_year"
```

### 4. Combining Features
You can combine filtering, searching, and ordering in a single request.

**Examples:**
```bash
# Search for "Django", filter by publication year 2023, order by title
GET /api/books/?search=Django&publication_year=2023&ordering=title

# Filter by author, order by publication year (descending)
GET /api/books/?author=William%20Vincent&ordering=-publication_year
```

**Using curl:**
```bash
curl "http://localhost:8000/api/books/?search=Django&ordering=-publication_year"
```

## Views Configuration

### BookListView
- **Type**: ListAPIView
- **Permission**: IsAuthenticatedOrReadOnly
- **Purpose**: Retrieve all books from the database
- **Access**: All users (authenticated and unauthenticated)
- **Features**:
  - **Filtering**: By title, author, publication_year
  - **Searching**: By title and author (partial match)
  - **Ordering**: By title and publication_year
  - **Default Ordering**: By title (ascending)

### BookDetailView
- **Type**: RetrieveAPIView
- **Permission**: IsAuthenticatedOrReadOnly
- **Purpose**: Retrieve a single book by its ID
- **Access**: All users (authenticated and unauthenticated)

### BookCreateView
- **Type**: CreateAPIView
- **Permission**: IsAuthenticated
- **Purpose**: Create a new book entry
- **Access**: Authenticated users only
- **Validation**: Automatic data validation via serializer

### BookUpdateView
- **Type**: UpdateAPIView
- **Permission**: IsAuthenticated
- **Purpose**: Update an existing book entry
- **Access**: Authenticated users only
- **Validation**: Automatic data validation via serializer

### BookDeleteView
- **Type**: DestroyAPIView
- **Permission**: IsAuthenticated
- **Purpose**: Delete a book entry
- **Access**: Authenticated users only

## Implementation Details

### Filter Backends
The API uses three Django REST Framework filter backends:

1. **DjangoFilterBackend**: Provides exact-match filtering on specified fields
2. **SearchFilter**: Enables partial text search across multiple fields
3. **OrderingFilter**: Allows sorting results by specified fields

### Configuration in views.py
```python
filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
filterset_fields = ['title', 'author', 'publication_year']
search_fields = ['title', 'author']
ordering_fields = ['title', 'publication_year']
ordering = ['title']  # Default ordering
```

## Testing the API

### Using Postman:
1. **List all books**: GET `http://localhost:8000/api/books/`
2. **Filter books**: GET `http://localhost:8000/api/books/?author=Author%20Name`
3. **Search books**: GET `http://localhost:8000/api/books/?search=keyword`
4. **Order books**: GET `http://localhost:8000/api/books/?ordering=-publication_year`
5. **Combined query**: GET `http://localhost:8000/api/books/?search=Django&ordering=title`

### Using curl:
```bash
# List all books
curl http://localhost:8000/api/books/

# Filter by author
curl "http://localhost:8000/api/books/?author=William%20Vincent"

# Search for "Django"
curl "http://localhost:8000/api/books/?search=Django"

# Order by publication year (descending)
curl "http://localhost:8000/api/books/?ordering=-publication_year"

# Combined: search and order
curl "http://localhost:8000/api/books/?search=Python&ordering=title"

# Create a book (requires authentication)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{"title":"New Book","author":"Author Name","publication_year":2024}'
```

## Setup Instructions
```bash
# Install dependencies
pip install django djangorestframework django-filter

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

## Permissions
- **IsAuthenticatedOrReadOnly**: Allows read access to everyone, but write access only to authenticated users
- **IsAuthenticated**: Restricts access to authenticated users only

## Dependencies
- Django
- Django REST Framework
- django-filter

## Testing

### Test Suite Overview
The project includes comprehensive unit tests for all API endpoints, covering:
- CRUD operations (Create, Read, Update, Delete)
- Filtering functionality
- Search functionality
- Ordering functionality
- Authentication and permissions
- Error handling and edge cases

### Running Tests

To run all tests:
```bash
python manage.py test api
```

To run tests with verbose output:
```bash
python manage.py test api --verbosity=2
```

To run a specific test class:
```bash
python manage.py test api.test_views.BookAPITestCase
```

To run a specific test method:
```bash
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated
```

### Test Cases

#### CRUD Operations Tests

1. **test_list_books**: Tests retrieving all books
   - Expected: 200 OK status, list of all books

2. **test_retrieve_book_detail**: Tests retrieving a single book
   - Expected: 200 OK status, correct book details

3. **test_create_book_authenticated**: Tests creating a book with authentication
   - Expected: 201 CREATED status, book created in database

4. **test_create_book_unauthenticated**: Tests creating a book without authentication
   - Expected: 403 FORBIDDEN status

5. **test_update_book_authenticated**: Tests updating a book with authentication
   - Expected: 200 OK status, book updated in database

6. **test_update_book_unauthenticated**: Tests updating a book without authentication
   - Expected: 403 FORBIDDEN status

7. **test_delete_book_authenticated**: Tests deleting a book with authentication
   - Expected: 204 NO CONTENT status, book removed from database

8. **test_delete_book_unauthenticated**: Tests deleting a book without authentication
   - Expected: 403 FORBIDDEN status

#### Filtering Tests

9. **test_filter_books_by_author**: Tests filtering books by author name
   - Expected: 200 OK status, only books by specified author

10. **test_filter_books_by_publication_year**: Tests filtering by publication year
    - Expected: 200 OK status, only books from specified year

#### Search Tests

11. **test_search_books**: Tests searching books by title or author
    - Expected: 200 OK status, books matching search query

#### Ordering Tests

12. **test_order_books_by_title**: Tests ordering books by title (ascending)
    - Expected: 200 OK status, books sorted alphabetically

13. **test_order_books_by_publication_year_descending**: Tests ordering by year (descending)
    - Expected: 200 OK status, books sorted newest to oldest

#### Combined Features Tests

14. **test_combined_filter_search_order**: Tests combining multiple query parameters
    - Expected: 200 OK status, all filters applied correctly

#### Error Handling Tests

15. **test_invalid_book_creation_missing_fields**: Tests creating book with missing fields
    - Expected: 400 BAD REQUEST status

16. **test_retrieve_nonexistent_book**: Tests retrieving a non-existent book
    - Expected: 404 NOT FOUND status

### Interpreting Test Results

#### Successful Test Run
```bash
----------------------------------------------------------------------
Ran 16 tests in 2.345s

OK
```

This indicates all tests passed successfully.

#### Failed Test Run
```bash
FAIL: test_create_book_authenticated (api.test_views.BookAPITestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
...
AssertionError: 403 != 201
```

This indicates a test failed. Review the error message and fix the issue.

### Test Coverage

To check test coverage (requires `coverage` package):
```bash
pip install coverage
coverage run --source='.' manage.py test api
coverage report
```

### Testing Strategy

1. **Setup**: Each test uses fresh test data created in `setUp()` method
2. **Isolation**: Tests are independent and don't affect each other
3. **Authentication**: Tests verify both authenticated and unauthenticated scenarios
4. **Edge Cases**: Tests include invalid data and non-existent resources
5. **Permissions**: Tests ensure proper access control enforcement

### Best Practices

- Run tests before committing code
- Add new tests when adding new features
- Keep tests focused on single functionality
- Use descriptive test names
- Document expected behavior in test docstrings