# Create Operation

Command: Create a Book instance with the title "1984", author "George Orwell", and publication year 1949.

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
Expected output: Book instance created successfully.
