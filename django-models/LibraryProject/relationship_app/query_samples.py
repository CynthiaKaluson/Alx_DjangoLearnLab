"""
Sample queries demonstrating model relationships
"""

def query_books_by_author(author_name):
    """
    Query all books by a specific author
    """
    from .models import Book, Author
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return Book.objects.none()

def list_books_in_library(library_name):
    """
    List all books in a library
    """
    from .models import Library
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return Library.objects.none()

def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library
    """
    from .models import Librarian, Library
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

# Example usage (commented out for ALX requirements)
if __name__ == "__main__":
    # Query all books by a specific author
    author_books = query_books_by_author("J.K. Rowling")
    print("Books by J.K. Rowling:", list(author_books))
    
    # List all books in a library
    library_books = list_books_in_library("Central Library")
    print("Books in Central Library:", list(library_books))
    
    # Retrieve the librarian for a library
    librarian = get_librarian_for_library("Central Library")
    print("Librarian for Central Library:", librarian)
EOFcat > relationship_app/query_samples.py << 'EOF'
"""
Sample queries demonstrating model relationships
"""

def query_books_by_author(author_name):
    """
    Query all books by a specific author
    """
    from .models import Book, Author
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return Book.objects.none()

def list_books_in_library(library_name):
    """
    List all books in a library
    """
    from .models import Library
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return Library.objects.none()

def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library
    """
    from .models import Librarian, Library
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

# Example usage (commented out for ALX requirements)
if __name__ == "__main__":
    # Query all books by a specific author
    author_books = query_books_by_author("J.K. Rowling")
    print("Books by J.K. Rowling:", list(author_books))
    
    # List all books in a library
    library_books = list_books_in_library("Central Library")
    print("Books in Central Library:", list(library_books))
    
    # Retrieve the librarian for a library
    librarian = get_librarian_for_library("Central Library")
    print("Librarian for Central Library:", librarian)
