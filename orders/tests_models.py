from django.test import TestCase
from django.contrib.auth.models import User
from django_countries.fields import Country
from inventory.models import Stock
from .models import Order, OrderLineItem


class OrderModelTestCase(TestCase):
    def setUp(self):
        # create a user for testing, if needed
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.country = Country(name='United States', code='US')
        self.country.save()
        self.stock = Stock.objects.create(
            book_title='Test Book',
            condition='New',
        )
        self.order = Order.objects.create(
            full_name='John Doe',
            email='johndoe@example.com',
            phone_number='1234567890',
            country=self.country,
            postcode='12345',
            town_or_city='City',
            street_address1='123 Street',
            street_address2='Apt 456',
            county='County',
            shipping_option=True
        )

    def test_generate_order_number(self):
        # test: the order_number is generated and is not empty
        self.assertTrue(self.order.order_number)

    def test_order_string_representation(self):
        # test: the string representation of an order is correct
        expected_str = 'John Doe, order number: \
            {}'.format(self.order.order_number)
        self.assertEqual(str(self.order), expected_str)


class OrderLineItemModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.country = Country(name='United States', code='US')
        self.country.save()
        self.stock = Stock.objects.create(
            book_title='Test Book',
            condition='New',
        )
        self.order = Order.objects.create(
            full_name='John Doe',
            email='johndoe@example.com',
            phone_number='1234567890',
            country=self.country,
            postcode='12345',
            town_or_city='City',
            street_address1='123 Street',
            street_address2='Apt 456',
            county='County',
            shipping_option=True
        )
        self.order_line_item = OrderLineItem.objects.create(
            order=self.order,
            stock_item=self.stock,
            quantity=2,
            lineitem_total=59.98  # Should be updated by save() method
        )

    def test_order_line_item_total(self):
        # test: lineitem_total is correctly calculated by the save() method
        expected_total = self.stock.price * self.order_line_item.quantity
        self.assertEqual(self.order_line_item.lineitem_total, expected_total)

    def test_order_line_item_string_representation(self):
        # test: the string representation of an order line item is correct
        expected_str = 'Test Book, condition: New, x 10 on order: \
            {}'.format(self.order.order_number)
        self.assertEqual(str(self.order_line_item), expected_str)
