# Update Operation

Command: Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
Expected output: Title updated to "Nineteen Eighty-Four".
