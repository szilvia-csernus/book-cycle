
def bag_contents(request):

    bag_items = []
    total = 0
    book_count = 0

    context = {
        'bag_items': bag_items,
        'total': total,
        'book_count': book_count,
    }

    return context
