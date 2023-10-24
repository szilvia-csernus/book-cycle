from django.test import TestCase
from orders.models import Order
from orders.forms import OrderForm


class OrderFormTests(TestCase):
    """ Test OrderForm """
    def test_order_form_valid(self):
        form_data = {
            'full_name': 'Emily Grant',
            'email': 'emilygrant@example.com',
            'phone_number': '1234567890',
            'street_address1': 'asdfgsadf',
            'town_or_city': 'Town',
            'postcode': '12345',
            'country': 'GB',
            'county': 'Berkshire',
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_post_invalid(self):
        # Test the form with missing required fields
        form_data = {
            'county': 'Berkshire',
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_order_form_save(self):
        form_data = {
            'full_name': 'Emily Grant',
            'email': 'emilygrant@example.com',
            'phone_number': '1234567890',
            'street_address1': 'asdfgsadf',
            'town_or_city': 'Town',
            'postcode': '12345',
            'country': 'GB',
            'county': 'Berkshire',
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertIsInstance(order, Order)
