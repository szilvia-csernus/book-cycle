from django.test import TestCase
from django.urls import reverse


class CheckoutViewTest(TestCase):

    def test_checkout_view_with_items_in_bag(self):
        response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('order_form', response.context)
        self.assertTemplateUsed(response, 'orders/checkout.html')
