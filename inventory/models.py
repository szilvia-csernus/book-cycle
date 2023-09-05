from django.db import models


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
        related_name='books_by_yea',
        on_delete=models.SET_NULL)
    subject = models.ForeignKey(
        'Subject',
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.SET_NULL)
    exam_board = models.CharField(max_length=254)
    publisher = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    product_url = models.URLField(max_length=1024, null=True, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Stock(models.Model):
    book = models.ForeignKey(
        'Book',
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(max_length=30)
    quantity = models.IntegerField(default=0)
