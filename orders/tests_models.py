from django.test import TestCase
from inventory.models import YearGroup, Subject, Book, Stock
from orders.models import Order, OrderLineItem


class OrderModelTestCase(TestCase):

    def setUp(self):
        # Set up test data for Order
        self.order = Order.objects.create(
            full_name='Emily Grant',
            email='emilygrant@example.com',
            phone_number='1234567890',
            country='GB',
            postcode='12345',
            town_or_city='City',
            street_address1='asdfhgf',
            shipping_required=True
        )

    def test_generate_order_number(self):
        # test: the order_number is generated and is not empty
        self.assertTrue(self.order.order_number)

    def test_order_string_representation(self):
        # test: the string representation of an order is correct
        expected_str = f'Emily Grant, order number: {self.order.order_number}'
        self.assertEqual(str(self.order), expected_str)


class OrderLineItemModelTestCase(TestCase):
    def setUp(self):
        year_group = YearGroup.objects.create(name="alevel")
        subject = Subject.objects.create(name="computing")
        book = Book.objects.create(
            title="Computer Science",
            year_group=year_group,
            subject=subject,
        )
        stock_new = Stock.objects.create(
            book=book,
            condition="new",
            price=10.00,
            quantity=10
        )
        stock_good = Stock.objects.create(
            book=book,
            condition="good",
            price=8.00,
            quantity=8
        )
        stock_fair = Stock.objects.create(
            book=book,
            condition="fair",
            price=5.00,
            quantity=2
        )
        order = Order.objects.create(
            full_name='Emily Grant',
            email='emilygrant@example.com',
            phone_number='1234567890',
            country='GB',
            postcode='12345',
            town_or_city='City',
            street_address1='asdfhgf',
            shipping_required=True
        )
        OrderLineItem.objects.create(
            order=order,
            stock=stock_new,
            quantity=2,
        )

    def test_order_line_item_total(self):
        order_line_item = OrderLineItem.objects.get(id=1)
        # test: lineitem_total is correctly calculated by the save() method
        self.assertEqual(order_line_item.lineitem_total, 20)

    def test_order_line_item_string_representation(self):
        order_line_item = OrderLineItem.objects.get(id=1)
        # test: the string representation of an order line item is correct
        self.assertIn(str('Computer Science', order_line_item))
