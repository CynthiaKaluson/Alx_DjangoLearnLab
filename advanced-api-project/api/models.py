"""
Data models for the API application.
Defines Author and Book models with a one-to-many relationship.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Author(models.Model):
    """
    Author model representing a book author.
    Has a one-to-many relationship with Book model.
    Each author can have multiple books.
    """
    name = models.CharField(
        max_length=200,
        help_text="Full name of the author"
    )

    def __str__(self):
        """String representation of the Author model."""
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    """
    Book model representing a published book.
    Linked to Author via ForeignKey (one-to-many relationship).
    """
    title = models.CharField(
        max_length=300,
        help_text="Title of the book"
    )
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000)
        ],
        help_text="Year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="Author who wrote the book"
    )

    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} by {self.author.name}"

    class Meta:
        ordering = ['title']
        verbose_name = "Book"
        verbose_name_plural = "Books"