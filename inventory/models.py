from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid


class YearGroup(models.Model):
    name = models.CharField(max_length=30)
    friendly_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=254)
    year_group = models.ForeignKey(
        'YearGroup',
        null=True,
        blank=False,
        related_name='books',
        on_delete=models.SET_NULL)
    subject = models.ForeignKey(
        'Subject',
        null=True,
        blank=False,
        related_name='books',
        on_delete=models.SET_NULL)
    exam_board = models.CharField(max_length=254, null=True, blank=True)
    publisher = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    product_url = models.URLField(max_length=1024, null=True, blank=True)
    slug = models.SlugField(max_length=254, null=False, unique=True)

    def __str__(self, *args, **kwargs):
        return self.title

    def save(self, *args, **kwargs):
        # Check if the book has no id (is now being created)
        if not self.id:
            # Create a new unique identifier,
            # but limit the length to 8 characters.
            new_uuid = str(uuid.uuid4())[:8]
            # Create a slug based on the new identifier and the book's title
            self.slug = slugify(f"{self.title}-{new_uuid}")
        super().save(*args, **kwargs)

    def get_slug_url(self):
        """ SEO friendly url """
        return reverse("book_detail", kwargs={"slug": self.slug})

    def in_stock(self):
        if len(self.stock_set.all()) == 0:
            return False
        in_stock = False
        for stock_book in self.stock_set.all():
            if stock_book.get_available_quantity() > 0:
                in_stock = True
        return in_stock

    def get_cheapest_stock(self):
        """Returns the cheapest stock or False if there is no stock object
        associated with the book."""
        if not self.in_stock():
            return False
        stocks = self.stock_set.all()

        cheapest_stock = None
        cheapest_price = None

        # Check each stock condition and update cheapest_stock and
        # cheapest_price if any
        for stock in stocks:
            if stock.get_available_quantity() > 0:
                price = stock.price
                if cheapest_price is None or price < cheapest_price:
                    cheapest_stock = stock
                    cheapest_price = price

        return cheapest_stock


class Stock(models.Model):
    book = models.ForeignKey(
        'Book',
        null=True,
        on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(max_length=30)
    quantity = models.IntegerField(default=0)
    blocked = models.IntegerField(default=0)

    def __str__(self, *args, **kwargs):
        return f'{self.book.title}, condition: {self.condition}'

    def get_available_quantity(self):
        available_quantity = self.quantity - self.blocked
        if available_quantity > 0:
            return available_quantity
        else:
            return 0

    def block_1_stock(self):
        if self.get_available_quantity() < 1:
            raise ValueError('Not enough stock available')
        else:
            self.blocked += 1
            self.save()

    def unblock_stock(self, quantity=1):
        if self.blocked < quantity:
            self.blocked = 0
        else:
            self.blocked -= quantity
        self.save()

    def reduce_stock(self, amount):
        if amount > self.quantity:
            raise ValueError('Not enough stock available')
        else:
            self.quantity -= amount
            self.blocked -= amount
            self.save()

    def add_stock(self, amount):
        self.quantity += amount
        self.save()
