from .models import Order


def manage_orders_details(request):
    """
    Order counts made available in context
    """

    orders_to_post_count = Order.objects.all() \
                                .filter(posted_on__isnull=True,
                                        picked_up_on__isnull=True,
                                        shipping_required=True) \
                                .count()

    orders_to_collect_count = Order.objects.all() \
                                   .filter(posted_on__isnull=True,
                                           picked_up_on__isnull=True,
                                           shipping_required=False) \
                                   .count()

    context = {
        'orders_to_post_count': orders_to_post_count,
        'orders_to_collect_count': orders_to_collect_count,
    }

    return context
