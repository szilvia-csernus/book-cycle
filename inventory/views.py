from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book


def all_books(request):
    """ A view to show all books, including sorting and search queries. """
    books = Book.objects.all()
    search_term = None
    year_group = None

    if request.GET:
        if 'search' in request.GET:
            search_term = request.GET['search']
            if not search_term:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('books'))

            search_queries = Q(title__icontains=search_term) | \
                Q(year_group__name__icontains=search_term) | \
                Q(subject__name__icontains=search_term)

            books = books.filter(search_queries)

        if 'year_group' in request.GET:
            year_group = request.GET['year_group']
            books = books.filter(year_group__name=year_group)

    context = {
        'books': books,
        'search_term': search_term,
        'year_group': year_group
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
