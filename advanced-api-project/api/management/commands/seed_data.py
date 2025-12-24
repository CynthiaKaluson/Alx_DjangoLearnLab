"""
Django management command to seed initial data.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Author, Book


class Command(BaseCommand):
    help = 'Seeds the database with initial author and book data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database with initial data...')

        # Create authors
        authors_data = [
            {'name': 'George Orwell', 'birth_date': '1903-06-25'},
            {'name': 'J.K. Rowling', 'birth_date': '1965-07-31'},
            {'name': 'J.R.R. Tolkien', 'birth_date': '1892-01-03'},
            {'name': 'Harper Lee', 'birth_date': '1926-04-28'},
        ]

        authors = []
        for data in authors_data:
            author, created = Author.objects.get_or_create(
                name=data['name'],
                defaults={'birth_date': data['birth_date']}
            )
            authors.append(author)
            if created:
                self.stdout.write(f'Created author: {author.name}')

        # Create books
        books_data = [
            {
                'title': '1984',
                'author': authors[0],
                'publication_year': 1949,
                'isbn': '9780451524935',
                'price': 9.99,
                'pages': 328,
                'genre': 'FICTION'
            },
            {
                'title': 'Animal Farm',
                'author': authors[0],
                'publication_year': 1945,
                'isbn': '9780451526342',
                'price': 7.99,
                'pages': 112,
                'genre': 'FICTION'
            },
            {
                'title': "Harry Potter and the Philosopher's Stone",
                'author': authors[1],
                'publication_year': 1997,
                'isbn': '9780747532743',
                'price': 12.99,
                'pages': 223,
                'genre': 'FANTASY'
            },
            {
                'title': 'The Hobbit',
                'author': authors[2],
                'publication_year': 1937,
                'isbn': '9780547928227',
                'price': 11.99,
                'pages': 310,
                'genre': 'FANTASY'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': authors[3],
                'publication_year': 1960,
                'isbn': '9780061120084',
                'price': 10.99,
                'pages': 281,
                'genre': 'FICTION'
            },
        ]

        for data in books_data:
            book, created = Book.objects.get_or_create(
                title=data['title'],
                author=data['author'],
                defaults={
                    'publication_year': data['publication_year'],
                    'isbn': data['isbn'],
                    'price': data['price'],
                    'pages': data['pages'],
                    'genre': data['genre']
                }
            )
            if created:
                self.stdout.write(f'Created book: {book.title} by {book.author.name}')

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))