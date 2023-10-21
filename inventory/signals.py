from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.sessions.models import Session

from .models import Stock


@receiver(pre_delete, sender=Session)
def un_block_stock(sender, instance, **kwargs):
    """ If the session is about to be deleted or expired, unblock the stock
    that was blocked by putting books in the shopping bag.
    """

    # Get the bag from the session
    bag = instance.get_decoded().get('bag', {})

    # Loop through the bag and unblock the stock
    for stock_id, quantity in bag.items():
        stock = Stock.objects.get(id=stock_id)
        stock.blocked -= quantity
        stock.save()
