from datetime import timedelta
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_POST
from .models import Book, Stock
from .forms import BookForm


def build_query_string(request):
    """
    Re-build the query string to use for redirecting back to the books page
    with all the filters applied.
    """
    query_string = ''

    if 'search' in request.GET:
        query_string = query_string + 'search=' + request.GET['search']

    if 'subject' in request.GET:
        query_string = query_string + '&subject=' + request.GET['subject']

    if 'year_group' in request.GET:
        query_string = query_string + '&year_group=' + \
            request.GET['year_group']

    if 'sort' in request.GET:
        query_string = query_string + '&sort=' + request.GET['sort']

    if 'direction' in request.GET:
        query_string = query_string + '&direction=' + request.GET['direction']

    return query_string


def all_books(request):
    """
    Show all books with all filters, sorting and search queries applied.
    """
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

            if search_term != 'None':
                # Q is used to combine search queries with OR
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
    """ Show and individual book's details. """

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

    query_string = build_query_string(request)

    context = {
        'book': book,
        'book_listing': book_listing,
        'redirect_query_string': query_string
    }

    return render(request, 'inventory/book_detail.html', context)


@permission_required('user.is_staff')
def add_book(request):
    """
    GET: Render form to add new book to the store.
    POST: Add new book to the store and create stock instances for
    each condition.
    """
    template = 'inventory/add_book.html'
    context = {}

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
            return redirect(reverse('manage_stock', args=[book.slug]))
        else:
            messages.error(request, 'Failed to add book. Please ensure the \
                           form is valid.')
            context['bookform'] = form
    else:
        form = BookForm()
        context['bookform'] = form

    return render(request, template, context)


@permission_required('user.is_staff')
def edit_book(request, slug):
    """ Edit the book's details or its prices. """

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
        # Check if the image has changed or if the user has removed the
        # image
        if 'image' in bookform.changed_data:
            # Delete the old image file
            if book.image:
                storage, path = book.image.storage, book.image.path
                if storage.exists(path):
                    storage.delete(path)

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
            return redirect(reverse('manage_stock', args=[book.slug]))
        else:
            messages.error(request, 'Failed to update book. Please ensure the \
                           form is valid.')
    else:
        bookform = BookForm(instance=book, initial=initial_data)
        messages.info(request, f'You are editing {book.title}')

    query_string = build_query_string(request)

    template = 'inventory/edit_book.html'
    context = {
        'bookform': bookform,
        'book': book,
        'redirect_query_string': query_string,
    }

    return render(request, template, context)


@permission_required('user.is_staff')
def delete_book(request, slug):
    """ Delete the book from the database. """

    book = get_object_or_404(Book, slug=slug)

    # Check if there are any orders for this book in the past year
    stocks = book.stock_set.all()
    for stock in stocks:
        orderlines = stock.orderlineitems.all()
        for orderline in orderlines:
            order = orderline.order
            if order.date + timedelta(days=365) > timezone.now():
                messages.error(request, 'Cannot delete book with orders\
                               in the past year.')
                return redirect(reverse('edit_book', args=[book.slug]))

    try:
        book.delete()
        messages.success(request, 'Book deleted!')
        return redirect(reverse('books'))

    except Exception as e:
        messages.error(request, 'Failed to delete book.', e)
        return redirect(reverse('book_detail', args=[book.slug]))


@permission_required('user.is_staff')
def manage_stock(request, slug):
    """ Show the book's details and stock data. """
    book = get_object_or_404(Book, slug=slug)

    stock_set = book.stock_set.all()
    book_listing = []

    conditions = ["new", "good", "fair"]

    for condition in conditions:
        condition_data = {}
        for stock in stock_set.filter(condition=condition):
            condition_data = {
                'id': stock.id,
                'condition': condition,
                'price': stock.price,
                'stock_quantity': stock.quantity,
                'stock_blocked': stock.blocked,
                'stock_available_quantity': stock.get_available_quantity(),
            }

        book_listing.append(condition_data)

    query_string = build_query_string(request)

    context = {
        'book': book,
        'book_listing': book_listing,
        'redirect_query_string': query_string
    }

    return render(request, 'inventory/manage_stock.html', context)


@require_POST
@permission_required('user.is_staff')
def add_stock(request, stock_id):
    """
    Increase the stock item's quantity.
    """

    stock = get_object_or_404(Stock, id=stock_id)
    redirect_url = request.POST.get('redirect_url')

    try:
        quantity = int(request.POST.get('quantity'))
        stock.add_stock(quantity)

        messages.success(request, 'Successfully added stock!')
        return redirect(redirect_url)
    except Exception:
        messages.error(request, 'Failed to add stock.')
        return redirect(redirect_url)


@require_POST
@permission_required('user.is_staff')
def reduce_stock(request, stock_id):
    """
    Reduce the stock item's quantity.
    """

    stock = get_object_or_404(Stock, id=stock_id)
    redirect_url = request.POST.get('redirect_url')

    try:
        quantity = int(request.POST.get('quantity'))
        stock.reduce_stock(quantity)

        messages.success(request, 'Successfully reduced stock!')
        return redirect(redirect_url)

    except Exception:
        messages.error(request, 'Failed to remove stock.')
        return redirect(redirect_url)
