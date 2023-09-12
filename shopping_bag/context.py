from django.shortcuts import get_object_or_404
from inventory.models import Stock


def bag_contents(request):

    bag_items = []
    total = 0
    book_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        stock_item = get_object_or_404(Stock, id=item_id)
        total += quantity * stock_item.price
        book_count += quantity
        bag_items.append({
            'id': item_id,
            'condition': stock_item.condition,
            'quantity': quantity,
            'stock_item': stock_item,
        })

    context = {
        'bag_items': bag_items,
        'total': total,
        'book_count': book_count,
    }

    return context
