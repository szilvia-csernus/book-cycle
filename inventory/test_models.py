from django.test import TestCase
from .models import YearGroup, Subject, Book, Stock
from decimal import Decimal


class TestModels(TestCase):

    def test_yeargroup_string_representation(self):
        year_group = YearGroup(name="Test YearGroup Name")
        self.assertEqual(str(year_group), year_group.name)

    def test_subject_string_representation(self):
        subject = Subject(name="Test Subject Name")
        self.assertEqual(str(subject), subject.name)

    def test_book_string_representation(self):
        book = Book.objects.create(title="Test Book Title")
        self.assertEqual(str(book), book.title)

    def test_slug_field_not_null(self):
        book = Book.objects.create(title="Test Book Title")
        self.assertIsNotNone(book.slug)

    def test_slug_field_is_unique(self):
        book1 = Book.objects.create(title="Test Book Title")
        book2 = Book.objects.create(title="Test Book Title")
        self.assertFalse(book1.slug == book2.slug)

    def test_in_stock_true(self):
        book = Book.objects.create(title="Test Book Title")
        Stock.objects.create(
            book=book,
            condition="new",
            price=Decimal("15.50"),
            quantity=23)
        in_stock = book.in_stock()
        self.assertTrue(in_stock)

    def test_in_stock_false(self):
        book = Book.objects.create(title="Test Book Title")
        in_stock = book.in_stock()
        self.assertFalse(in_stock)

    def test_cheapest_stock(self):
        book = Book.objects.create(title="Test Book Title")
        Stock.objects.create(
            book=book,
            condition="new",
            price=Decimal("15.50"),
            quantity=23)
        Stock.objects.create(
            book=book,
            condition="good",
            price=Decimal("12"),
            quantity=2)
        Stock.objects.create(
            book=book,
            condition="fair",
            price=Decimal("10"),
            quantity=3)
        cheapest_stock = book.get_cheapest_stock()
        self.assertEqual(cheapest_stock.quantity, 3)
