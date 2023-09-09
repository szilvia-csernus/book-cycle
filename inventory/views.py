from django.shortcuts import render, get_object_or_404
from .models import Book


def all_books(request):
    """ A view to show all books, including sorting and search queries. """
    books = Book.objects.all()

    context = {
        'books': books
    }
    return render(request, 'inventory/books.html', context)


def book_detail(request, slug):
    """ A view to show book details. """
    book = get_object_or_404(Book, slug=slug)
    stock = book.stock_set.all()
    context = {
        'book': book,
        'stock': stock
    }
    return render(request, 'inventory/book_detail.html', context)
