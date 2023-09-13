from django.shortcuts import get_object_or_404
from inventory.models import Stock, Book


def bag_contents(request):
    """ A view to return the shopping bag page """

    total = 0
    book_count = 0
    bag = request.session.get('bag', {})

    # create a dictionary of books from the bag in session
    book_list = {}
    for item_id, quantity in bag.items():
        stock_item = get_object_or_404(Stock, id=item_id)
        book = get_object_or_404(Book, id=stock_item.book.id)
        line_total = quantity * stock_item.price
        total += line_total
        book_count += quantity
        if quantity > 0:
            if book.id not in book_list:
                book_list[book.id] = {}
            if stock_item.condition not in book_list[book.id]:
                book_list[book.id].update({stock_item.condition: {}})
            book_list[book.id][stock_item.condition].update({
                        'id': item_id,
                        'condition': stock_item.condition,
                        'price': stock_item.price,
                        'quantity': quantity,
                        'line_total': line_total,
                    })

    # create an easily iterable list of books from the dictionary where "new",
    # "good" and "fair" are always in the same order
    bag_items = []
    for book_id, properties in book_list.items():
        book = get_object_or_404(Book, id=book_id)
        book_array = [book, [None, None, None]]
        if 'new' in properties.keys():
            book_array[1][0] = properties['new']
        if 'good' in properties.keys():
            book_array[1][1] = properties['good']
        if 'fair' in properties.keys():
            book_array[1][2] = properties['fair']

        bag_items.append(book_array)

    print('bag_items', bag_items)

    context = {
        'book_list': book_list,
        'bag_items': bag_items,
        'grand_total': total,
        'book_count': book_count,
    }

    return context
