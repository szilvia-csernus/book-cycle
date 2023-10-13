from django.test import TestCase
from inventory.models import YearGroup, Subject, Book, Stock
from orders.models import Order, OrderLineItem
from django.contrib.auth.models import User


class OrderModelTestCase(TestCase):

    def setUp(self):
        # Set up test data for Order
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
        OrderLineItem.objects.create(
            order=self.order,
            stock=stock_new,
            quantity=2,
        )
        # Create a user with staff permissions
        self.user = User.objects.create_user(
            username='staffmember',
            password='staffpassword',
            is_staff=True
        )

    def test_generate_order_number(self):
        # test: the order_number is generated and is not empty
        self.assertTrue(self.order.order_number)

    def test_order_total(self):
        # test: order_total is correctly calculated by the save() method
        self.assertEqual(self.order.order_total, 20)

    def test_update_posted(self):
        # test: update_posted method updates posted_on and posted_by fields
        self.order.update_posted(self.user, '1234567890')
        self.assertTrue(self.order.posted_on)
        self.assertEqual(self.order.posted_by, self.user)
        self.assertEqual(self.order.tracking_number, '1234567890')

    def test_update_picked_up(self):
        # test: update_picked_up method updates picked_up_on and picked_up_by
        # fields
        self.order.update_picked_up('Peppa Pig')
        self.assertTrue(self.order.picked_up_on)
        self.assertEqual(self.order.picked_up_by, 'Peppa Pig')

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
        self.orderline_item = OrderLineItem.objects.create(
            order=order,
            stock=stock_new,
            quantity=2,
        )

    def test_order_line_item_total(self):
        # test: lineitem_total is correctly calculated by the save() method
        self.assertEqual(self.orderline_item.lineitem_total, 20)

    def test_order_line_item_string_representation(self):
        # test: the string representation of an order line item is correct
        self.assertIn('Computer Science', str(self.orderline_item))
