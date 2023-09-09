from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid


class YearGroup(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=254)
    year_group = models.ForeignKey(
        'YearGroup',
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.SET_NULL)
    subject = models.ForeignKey(
        'Subject',
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.SET_NULL)
    exam_board = models.CharField(max_length=254, null=True, blank=True)
    publisher = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    product_url = models.URLField(max_length=1024, null=True, blank=True)
    slug = models.SlugField(null=False, unique=True)

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
            if stock_book.quantity > 0:
                in_stock = True
        return in_stock

    def get_book_stock(self):
        """ Returns book's stock in a convenient object format, like:
        {
          "new":
            {"condition": "new", "price": Decimal("25.00"), "quantity": 34},
          "good":
            {"condition": "good", "price": Decimal("20.00"), "quantity": 3},
          "fair":
            {"condition": "fair", "price": Decimal("15.00"), "quantity": 12}
        }
        """
        if not self.in_stock():
            return False

        stock = {
            "new":
                {"condition": "new", "price": "", "quantity": 0},
            "good":
                {"condition": "good", "price": "", "quantity": 0},
            "fair":
                {"condition": "fair", "price": "", "quantity": 0}
            }

        stock_set = self.stock_set.all()
        for stock_book in stock_set:
            details = {
                "condition": stock_book.condition,
                "price": stock_book.price,
                "quantity": stock_book.quantity
            }
            stock[stock_book.condition] = details
        return stock

    def get_cheapest_stock(self):
        """Returns the cheapest stock or False if there is no stock object
        associated with the book."""
        if not self.in_stock():
            return False
        stocks = self.get_book_stock()

        cheapest_stock = None
        cheapest_price = None

        # Check each stock condition and update cheapest_stock and
        # cheapest_price if any
        for condition, stock_data in stocks.items():
            if stock_data["quantity"] > 0:
                price = stock_data["price"]
                if cheapest_price is None or price < cheapest_price:
                    cheapest_stock = stock_data
                    cheapest_price = price

        if cheapest_stock is not None:
            return cheapest_stock
        else:
            return False

    def get_cheapest_stock_condition(self):
        """Returns the cheapest stock's condition."""
        cheapest_stock = self.get_cheapest_stock()
        if cheapest_stock:
            return cheapest_stock["condition"]
        return False

    def get_cheapest_stock_price(self):
        """Returns the cheapest stock's price."""
        cheapest_stock = self.get_cheapest_stock()
        if cheapest_stock:
            return cheapest_stock["price"]
        return False

    def get_cheapest_stock_quantity(self):
        """Returns the cheapest stock's quantity."""
        cheapest_stock = self.get_cheapest_stock()
        if cheapest_stock:
            return cheapest_stock["quantity"]
        return False


class Stock(models.Model):
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField(default=0)
