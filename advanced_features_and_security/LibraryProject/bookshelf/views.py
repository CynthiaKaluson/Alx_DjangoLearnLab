from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

# Secure view - uses ORM to prevent SQL injection
def book_list(request):
    # Safe query using Django ORM - prevents SQL injection
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})