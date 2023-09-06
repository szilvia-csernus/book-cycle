from django.shortcuts import render
from .models import Book


def all_books(request):
    """ A view to show all books, including sorting and search queries. """

    books = Book.objects.all()

    context = {
        'books': books
    }

    return render(request, 'inventory/books.html', context)
