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


class TestBookModel(TestCase):

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
        self.assertEqual(cheapest_stock.get_available_quantity(), 3)
        Stock.objects.all().delete()

    def test_cheapest_stock_when_no_stock(self):
        book = Book.objects.create(title="Test Book Title")
        cheapest_stock = book.get_cheapest_stock()
        self.assertFalse(cheapest_stock)

    def test_cheapest_stock_when_all_stock_zero(self):
        book = Book.objects.create(title="Test Book Title")
        Stock.objects.create(
            book=book,
            condition="new",
            price=Decimal("15.50"),
            quantity=0)
        Stock.objects.create(
            book=book,
            condition="good",
            price=Decimal("12"),
            quantity=0)
        Stock.objects.create(
            book=book,
            condition="fair",
            price=Decimal("10"),
            quantity=0)
        cheapest_stock = book.get_cheapest_stock()
        self.assertFalse(cheapest_stock)


class TestStockModel(TestCase):
    def setUp(self):
        # Create a book for testing
        self.book = Book.objects.create(title="Test Book")
        self.stock = Stock.objects.create(
            book=self.book,
            price=25.99,
            condition="New",
            quantity=100,
            blocked=10)

    def test_available_quantity_calculation(self):
        # test the available quantity is calculated correctly
        self.assertEqual(self.stock.get_available_quantity(), 90)

    def test_block_stock(self):
        # test blocking a certain amount of stock
        self.stock.block_stock(20)
        self.assertEqual(self.stock.blocked, 30)

    def test_block_stock_with_insufficient_available_quantity(self):
        # test that attempting to block more than available
        # quantity raises an error
        with self.assertRaises(ValueError):
            self.stock.block_stock(200)

    def test_reduce_stock(self):
        # test reducing stock
        self.stock.reduce_stock(5)
        self.assertEqual(self.stock.quantity, 95)
        self.assertEqual(self.stock.blocked, 5)

    def test_reduce_stock_with_insufficient_available_quantity(self):
        # Ensure that attempting to reduce more stock than available
        # quantity sets it to 0

        with self.assertRaises(ValueError):
            self.stock.reduce_stock(105)
        self.assertEqual(self.stock.quantity, 100)
        self.assertEqual(self.stock.blocked, 10)
