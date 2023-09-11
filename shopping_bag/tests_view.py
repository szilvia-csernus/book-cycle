from django.test import TestCase
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from .views import add_to_bag


class ShoppingBagViewTestCase(TestCase):

    def test_shopping_bag(self):
        response = self.client.get('/shopping_bag/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_bag/bag.html')


class AddToBagTestCase(TestCase):

    def setUp(self):
        # create a request factory
        self.factory = RequestFactory()

    def test_add_to_bag_new_book(self):
        # create a mock request object
        request = self.factory.post(reverse('add_to_bag'))
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        stock_id = 1
        request.POST['redirect_url'] = '/checkout/'

        response = add_to_bag(request, stock_id)

        # check if the book was added to the session
        self.assertEqual(request.session['bag'][str(stock_id)], 1)

        # check if the response redirects to the correct URL
        self.assertRedirects(response, '/checkout/')

    def test_add_to_bag_existing_book(self):
        # mock request with an existing book in the bag
        request = self.factory.post(reverse('add_to_bag'))
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session['bag'] = {'1': 2, '2': 1}
        request.session.save()

        stock_id = 1
        request.POST['redirect_url'] = '/shop/'

        response = add_to_bag(request, stock_id)

        # check if the quantity of the item in the session is incremented
        self.assertEqual(request.session['bag'][str(stock_id)], 3)

        # check if the response redirects to the correct URL
        self.assertRedirects(response, '/shop/')

    def test_add_to_bag_missing_redirect_url(self):
        # mock request without the redirect_url in POST data
        request = self.factory.post(reverse('add_to_bag'))
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        stock_id = 1

        add_to_bag(request, stock_id)

        # Check if the item was added to the session
        self.assertEqual(request.session['bag'][str(stock_id)], 1)

        # Check if the redirect URL is not set
        self.assertIsNone(request.session.get('redirect_url'))
