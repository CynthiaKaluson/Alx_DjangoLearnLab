from django.http import HttpResponse
from django.views.generic import DetailView

from .models import Book, Library


# Function-based view
def list_books(request):
    books = Book.objects.all()
    response = ""

    for book in books:
        response += f"{book.title} by {book.author.name}\n"

    return HttpResponse(response, content_type="text/plain")


# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
