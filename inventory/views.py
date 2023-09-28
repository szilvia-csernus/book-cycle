from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages
from .models import Book, Stock
from .forms import BookForm


def all_books(request):
    """ A view to show all books, including sorting and search queries. """
    books = Book.objects.all()
    search_term = None
    search_queries = None
    year_group = None
    subject = None
    sort = None
    direction = None
    query = Q()  # Initialize an empty Q object

    if request.GET:
        if 'sort' in request.GET:
            sort = request.GET['sort']
            sortkey = sort

            if sortkey == 'title':
                sortkey = 'lower_title'
                books = books.annotate(lower_title=Lower('title'))

            if sortkey == 'subject':
                sortkey = 'subject__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

        else:
            sort = 'title'
            sortkey = 'lower_title'
            direction = 'asc'
            books = books.annotate(lower_title=Lower('title'))

        books = books.order_by(sortkey)

        if 'search' in request.GET:
            search_term = request.GET['search']

            if search_term != 'None':  # Combine search queries with OR
                search_queries = (
                    Q(title__icontains=search_term) |
                    Q(year_group__name__icontains=search_term) |
                    Q(subject__name__icontains=search_term)
                )

                query &= search_queries  # Combine search queries with AND

        if 'year_group' in request.GET:
            year_group = request.GET['year_group']
            if year_group != 'None':
                query &= Q(year_group__name=year_group)

        if 'subject' in request.GET:
            subject = request.GET['subject']
            if subject != 'None':
                query &= Q(subject__name=subject)

        books = books.filter(query)  # Apply the combined query

    else:
        sort = 'title'
        sortkey = 'lower_title'
        direction = 'asc'
        books = books.annotate(lower_title=Lower('title'))

        books = books.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'
    query_string = request.GET.urlencode()
    context = {
        'books': books,
        'search_term': search_term,
        'year_group': year_group,
        'subject': subject,
        'current_sorting': current_sorting,
        'query_string': query_string,
    }

    return render(request, 'inventory/books.html', context)


def book_detail(request, slug):
    """ A view to show book details. """
    book = get_object_or_404(Book, slug=slug)

    stock_set = book.stock_set.all()
    bag = request.session.get('bag', {})
    book_listing = []

    conditions = ["new", "good", "fair"]

    for condition in conditions:
        condition_data = {}
        for stock in stock_set.filter(condition=condition):
            in_bag = str(stock.id) in list(bag.keys()) and \
                     bag[str(stock.id)] > 0
            bag_quantity = int(bag[str(stock.id)]) if in_bag else 0

            condition_data = {
                'id': stock.id,
                'in_bag': in_bag,
                'condition': condition,
                'price': stock.price,
                'stock_available_quantity': stock.get_available_quantity(),
                'bag_quantity': bag_quantity
            }

        book_listing.append(condition_data)

    # Re-build the query string to use for redirecting back to the books page
    # with all the same filters applied.
    query_string = ''

    if 'search' in request.GET:
        query_string = query_string + 'search=' + request.GET['search']
        print('search', query_string)

    if 'subject' in request.GET:
        query_string = query_string + '&subject=' + request.GET['subject']
        print('subject', query_string)

    if 'year_group' in request.GET:
        query_string = query_string + '&year_group=' + \
            request.GET['year_group']
        print('year_group', query_string)

    if 'sort' in request.GET:
        query_string = query_string + '&sort=' + request.GET['sort']
        print('sort', query_string)

    if 'direction' in request.GET:
        query_string = query_string + '&direction=' + request.GET['direction']
        print('direction', query_string)

    context = {
        'book': book,
        'book_listing': book_listing,
        'redirect_query_string': query_string
    }

    return render(request, 'inventory/book_detail.html', context)


def add_book(request):
    """
    Add a book to the store and create stock instances for each condition.
    """

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # After saving book, we can refer to it when creating new stock
            # instances
            book = form.save()

            # Create stock instances for 'new,' 'good,' and 'fair' conditions
            Stock.objects.create(book=book, condition='new',
                                 price=form.cleaned_data['stock_new_price'])
            Stock.objects.create(book=book, condition='good',
                                 price=form.cleaned_data['stock_good_price'])
            Stock.objects.create(book=book, condition='fair',
                                 price=form.cleaned_data['stock_fair_price'])

            messages.success(request, 'Successfully added book!')
            return redirect(reverse('book_detail', args=[book.slug]))
        else:
            messages.error(request, 'Failed to add book. Please ensure the \
                           form is valid.')
    else:
        bookform = BookForm()
        template = 'inventory/add_book.html'
        context = {
            'bookform': bookform,
        }
    return render(request, template, context)


def edit_book(request, slug):
    """ Edit a book or its prices in the store. """
    book = get_object_or_404(Book, slug=slug)

    # get the book's current prices to pre-populate the form
    initial_data = {
        'stock_new_price':
            book.stock_set.filter(condition='new').first().price,
        'stock_good_price':
            book.stock_set.filter(condition='good').first().price,
        'stock_fair_price':
            book.stock_set.filter(condition='fair').first().price,
    }
    if request.method == 'POST':
        bookform = BookForm(request.POST, request.FILES, instance=book)
        if bookform.is_valid():
            bookform.save()
            for stock in book.stock_set.all():
                if stock.condition == 'new':
                    stock.price = bookform.cleaned_data['stock_new_price']
                elif stock.condition == 'good':
                    stock.price = bookform.cleaned_data['stock_good_price']
                elif stock.condition == 'fair':
                    stock.price = bookform.cleaned_data['stock_fair_price']
                stock.save()

            messages.success(request, 'Successfully updated book!')
            return redirect(reverse('book_detail', args=[book.slug]))
        else:
            messages.error(request, 'Failed to update book. Please ensure the \
                           form is valid.')
    else:
        bookform = BookForm(instance=book, initial=initial_data)
        messages.info(request, f'You are editing {book.title}')

    template = 'inventory/edit_book.html'
    context = {
        'bookform': bookform,
        'book': book,
    }

    return render(request, template, context)


def delete_book(request, slug):
    """ Delete a book from the store. """
    book = get_object_or_404(Book, slug=slug)
    try:
        book.delete()
        messages.success(request, 'Book deleted!')
        return redirect(reverse('books'))

    except Exception as e:
        messages.error(request, 'Failed to delete book.', e)
        return redirect(reverse('book_detail', args=[book.slug]))
