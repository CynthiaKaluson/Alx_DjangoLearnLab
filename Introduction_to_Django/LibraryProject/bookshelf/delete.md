# Delete Operation

Command: Delete the book you created and confirm the deletion by trying to retrieve all books again.

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
books = Book.objects.all()
print(f"Books count: {books.count()}")
Expected output: Books count: 0
