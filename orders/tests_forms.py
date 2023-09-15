from django.test import TestCase
from orders.models import Order
from orders.forms import OrderFormPost, OrderFormPickup


class OrderFormTests(TestCase):
    def test_order_form_post_valid(self):
        form_data = {
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Main St',
            'town_or_city': 'City',
            'postcode': '12345',
            'country': 'US',
            'county': 'County',
        }
        form = OrderFormPost(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_post_invalid(self):
        # Test the form with missing required fields
        form_data = {}
        form = OrderFormPost(data=form_data)
        self.assertFalse(form.is_valid())

    def test_order_form_pickup_valid(self):
        form_data = {
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'postcode': '12345',
            'county': 'County',
        }
        form = OrderFormPickup(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_pickup_invalid(self):
        # Test the form with missing required fields
        form_data = {}
        form = OrderFormPickup(data=form_data)
        self.assertFalse(form.is_valid())

    def test_order_form_post_save(self):
        form_data = {
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Main St',
            'town_or_city': 'City',
            'postcode': '12345',
            'country': 'US',
            'county': 'County',
        }
        form = OrderFormPost(data=form_data)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertIsInstance(order, Order)

    def test_order_form_pickup_save(self):
        form_data = {
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'postcode': '12345',
            'county': 'County',
        }
        form = OrderFormPickup(data=form_data)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertIsInstance(order, Order)
