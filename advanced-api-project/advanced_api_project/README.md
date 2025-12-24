# Advanced API Project - Book Management API

## Overview
This project implements a RESTful API for managing books using Django REST Framework with custom views and generic views.

## API Endpoints

### Public Endpoints (Read-Only Access)
- `GET /api/books/` - List all books
- `GET /api/books/<int:pk>/` - Retrieve a single book by ID

### Protected Endpoints (Authentication Required)
- `POST /api/books/create/` - Create a new book
- `PUT /api/books/update/<int:pk>/` - Update an existing book
- `DELETE /api/books/delete/<int:pk>/` - Delete a book

## Views Configuration

### BookListView
- **Type**: ListAPIView
- **Permission**: IsAuthenticatedOrReadOnly
- **Purpose**: Retrieve all books from the database
- **Access**: All users (authenticated and unauthenticated)

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

## Permissions
- **IsAuthenticatedOrReadOnly**: Allows read access to everyone, but write access only to authenticated users
- **IsAuthenticated**: Restricts access to authenticated users only

## Testing the API

### Using curl:
```bash
# List all books
curl http://localhost:8000/api/books/

# Get a single book
curl http://localhost:8000/api/books/1/

# Create a book (requires authentication)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{"title":"New Book","author":"Author Name","publication_year":2024}'

# Update a book (requires authentication)
curl -X PUT http://localhost:8000/api/books/update/1/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{"title":"Updated Book","author":"Author Name","publication_year":2024}'

# Delete a book (requires authentication)
curl -X DELETE http://localhost:8000/api/books/delete/1/ \
  -u username:password
```

### Using Postman:
1. Import the endpoints into Postman
2. For protected endpoints, use Basic Auth with username/password
3. Test each endpoint with appropriate HTTP methods

## Setup Instructions
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```