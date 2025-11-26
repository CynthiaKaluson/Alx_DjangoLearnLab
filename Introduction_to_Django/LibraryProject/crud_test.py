import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from bookshelf.models import Book


def test_crud_operations():
    print("=== CRUD Operations Test ===")

    # CREATE
    print("\n1. CREATE Operation:")
    book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
    print(f"Created book: {book.title}")

    # RETRIEVE
    print("\n2. RETRIEVE Operation:")
    retrieved_book = Book.objects.get(title="1984")
    print(
        f"Retrieved: Title: {retrieved_book.title}, Author: {retrieved_book.author}, Year: {retrieved_book.publication_year}")

    # UPDATE
    print("\n3. UPDATE Operation:")
    retrieved_book.title = "Nineteen Eighty-Four"
    retrieved_book.save()
    print(f"Updated title to: {retrieved_book.title}")

    # DELETE
    print("\n4. DELETE Operation:")
    retrieved_book.delete()
    count = Book.objects.count()
    print(f"Books in database after deletion: {count}")

    print("\n=== All CRUD operations completed successfully ===")


if __name__ == "__main__":
    test_crud_operations()