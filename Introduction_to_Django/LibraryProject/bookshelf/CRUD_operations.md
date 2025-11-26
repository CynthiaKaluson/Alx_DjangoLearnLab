# Complete CRUD Operations

## Create
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
Retrieve
python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
Expected output: Title: 1984, Author: George Orwell, Year: 1949

Update
python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
Delete
python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
books = Book.objects.all()
print(f"Books count: {books.count()}")
Expected output: Books count: 0
