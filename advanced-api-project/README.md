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