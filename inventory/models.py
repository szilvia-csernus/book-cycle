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

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"slug": self.slug})


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
