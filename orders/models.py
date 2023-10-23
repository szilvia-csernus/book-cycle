import uuid
from django.utils import timezone

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django_countries.fields import CountryField

from inventory.models import Stock
from profiles.models import UserProfile

from django.contrib.auth import get_user_model
User = get_user_model()


class Order(models.Model):
    """ Model to store order data """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    shipping_required = models.BooleanField(default=False)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    # original bag is used when the webhook can't find the order in the db
    # and creates a new one
    original_bag = models.TextField(null=False, blank=False, default='')
    # the payment intent id
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')
    posted_on = models.DateTimeField(default=None, null=True, blank=True)
    posted_by = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='orders_posted')
    tracking_number = models.CharField(max_length=80, null=True, blank=True)
    picked_up_on = models.DateTimeField(default=None, null=True, blank=True)
    picked_up_by = models.CharField(max_length=50, null=True, blank=True)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def get_book_count(self):
        """
        Get the total number of books in the order.
        """
        return sum(item.quantity for item in self.lineitems.all())

    def update_delivery_cost(self):
        """
        Update delivery cost based on the shipping option selected.
        """
        if self.shipping_required:
            self.delivery_cost = settings.SHIPPING_COST
            self.save()

    def update_total(self):
        """
        Update grand total each time a line item is added, accounting for
        delivery costs as well.
        """
        # This method uses the lineitems reverse relationship. The
        # aggregate() method adds a default key called 'lineitem_total__sum'
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def update_posted(self, user, tracking_number=None):
        """
        Update posted_on and posted_by fields
        """
        self.posted_on = timezone.now()
        self.posted_by = user
        self.tracking_number = tracking_number
        self.save()

    def update_picked_up(self, collected_by):
        """
        Update picked_up_on and picked_up_by fields
        """
        self.picked_up_on = timezone.now()
        self.picked_up_by = collected_by
        self.save()

    def __str__(self):
        return f'{self.full_name}, order number: {self.order_number}'


class OrderLineItem(models.Model):
    """ Model to store order line item data """
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    stock = models.ForeignKey(Stock, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='orderlineitems')
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.stock.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.stock.book.title},\
            condition: {self.stock.condition},\
            x {self.quantity}\
            on order: {self.order.order_number}'
