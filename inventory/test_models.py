from django.test import TestCase
from .models import YearGroup, Subject, Book, Stock
from django.urls import reverse


class YearGroupModelTest(TestCase):

    def test_string_representation(self):
        # Create a YearGroup instance and test its string representation
        YearGroup.objects.create(name="alevel", friendly_name="A Level")
        year_group = YearGroup.objects.get(id=1)
        self.assertEqual(str(year_group), "alevel")
        self.assertEqual(str(year_group.friendly_name), "A Level")


class SubjectModelTest(TestCase):

    def test_string_representation(self):
        # Create a Subject instance and test its string representation
        Subject.objects.create(name="computing",
                               friendly_name="Computer Science")
        subject = Subject.objects.get(id=1)
        self.assertEqual(str(subject), "computing")
        self.assertEqual(str(subject.friendly_name), "Computer Science")


class BookModelTest(TestCase):

    def setUp(self):
        # Set up test data for YearGroup and Subject and a Book
        year_group = YearGroup.objects.create(name="alevel")
        subject = Subject.objects.create(name="computing")
        Book.objects.create(
            title="Computer Science",
            year_group=year_group,
            subject=subject,
            image_url="http://example.com/computing.jpg",
            product_url="http://example.com/computing",
        )

    def test_string_representation(self):
        # Test book's string representation
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), "Computer Science")

    def test_slug_creation(self):
        book = Book.objects.get(id=1)
        # The 'save' method should automatically generate a slug
        self.assertTrue(book.slug)

    def test_get_slug_url(self):
        book = Book.objects.get(id=1)
        # The get_slug_url method should return the full url for the book,
        # when the slug is appended to the 'book_detail' url
        url = reverse("book_detail", kwargs={"slug": book.slug})
        self.assertEqual(book.get_slug_url(), url)

    def test_in_stock(self):
        book = Book.objects.get(id=1)
        # Test in_stock method when there is no stock
        in_stock = book.in_stock()
        self.assertFalse(in_stock)
        # Test in_stock method when there is stock
        Stock.objects.create(
            book=book,
            condition="new",
            price=10.00,
            quantity=10
        )
        in_stock = book.in_stock()
        self.assertTrue(in_stock)

    def test_get_stock_methods(self):
        book = Book.objects.get(id=1)
        # Test get_stock methods when there is no stock
        cheapest_stock = book.get_cheapest_stock()
        self.assertEqual(cheapest_stock, False)
        self.assertEqual(book.get_stock_new(), False)
        self.assertEqual(book.get_stock_good(), False)
        self.assertEqual(book.get_stock_fair(), False)
        # Test get_stock methods when there is stock
        new = Stock.objects.create(
            book=book,
            condition="new",
            price=10.00,
            quantity=10
        )
        good = Stock.objects.create(
            book=book,
            condition="good",
            price=8.00,
            quantity=8
        )
        fair = Stock.objects.create(
            book=book,
            condition="fair",
            price=5.00,
            quantity=2
        )
        cheapest_stock = book.get_cheapest_stock()
        self.assertEqual(cheapest_stock, fair)
        self.assertEqual(book.get_stock_new(), new)
        self.assertEqual(book.get_stock_good(), good)
        self.assertEqual(book.get_stock_fair(), fair)

    def test_delete_book(self):
        book = Book.objects.get(id=1)
        # Delete the only book in the database
        book.delete()
        self.assertEqual(Book.objects.count(), 0)


class StockModelTest(TestCase):

    def setUp(self):
        # Set up test data for Book and a Stock item
        book = Book.objects.create(title="Computing")
        Stock.objects.create(
            book=book,
            price=10.00,
            condition="new",
            quantity=10,
            blocked=3
        )
        Stock.objects.create(
            book=book,
            condition="good",
            price=8.00,
            quantity=0,
            blocked=0
        )

    def test_string_representation(self):
        stock = Stock.objects.get(id=1)
        # Test stock's string representation
        self.assertEqual(str(stock), "Computing, condition: new")

    def test_get_available_quantity(self):
        stock_new = Stock.objects.get(id=1)
        stock_good = Stock.objects.get(id=2)
        # Available quantity is quantity - blocked
        self.assertEqual(stock_new.get_available_quantity(), 7)
        self.assertEqual(stock_good.get_available_quantity(), 0)

    def test_block_1_stock(self):
        stock_new = Stock.objects.get(id=1)
        stock_good = Stock.objects.get(id=2)
        # Test if blocked stock is increased by 1
        stock_new.block_1_stock()
        self.assertEqual(stock_new.blocked, 4)
        # Test if blocked stock is not increased when there is no stock
        with self.assertRaises(ValueError):
            stock_good.block_1_stock()
            self.assertEqual(stock_good.blocked, 0)

    def test_unblock_stock(self):
        stock_new = Stock.objects.get(id=1)
        stock_good = Stock.objects.get(id=2)
        # Test if blocked stock is decreased
        stock_new.unblock_stock(2)
        self.assertEqual(stock_new.blocked, 1)
        # Test if blocked stock is not decreased when blocked is less
        stock_good.unblock_stock(2)
        self.assertEqual(stock_good.blocked, 0)

    def test_reduce_stock_by_purchase(self):
        stock_new = Stock.objects.get(id=1)
        stock_good = Stock.objects.get(id=2)
        # This method should decrease both the quantity and the blocked amounts
        stock_new.reduce_stock_by_purchase(2)
        self.assertEqual(stock_new.quantity, 8)
        self.assertEqual(stock_new.blocked, 1)
        # Test if the method raises an error when there is not enough stock
        with self.assertRaises(ValueError):
            stock_good.reduce_stock_by_purchase(2)
            self.assertEqual(stock_good.quantity, 0)
            self.assertEqual(stock_good.blocked, 0)

    def test_add_stock(self):
        stock = Stock.objects.get(id=1)
        # This method should increase the stock quantity
        stock.add_stock(5)
        self.assertEqual(stock.quantity, 15)

    def test_reduce_stock(self):
        stock = Stock.objects.get(id=1)
        # This method should decrease the stock quantity
        stock.reduce_stock(2)
        self.assertEqual(stock.quantity, 8)
