from django.test import TestCase


class ShoppingBagViewTestCase(TestCase):

    def test_shopping_bag(self):
        response = self.client.get('/shopping_bag/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_bag/bag.html')
