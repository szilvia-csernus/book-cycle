from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Stock


class TestViews(TestCase):

    def test_all_books(self):
        response = self.client.get('/books/all_books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/all_books.html')

    def test_add_book_unauthorized(self):
        response = self.client.post('/books/add/', {'title': 'Test Book'})
        self.assertEqual(response.status_code, 401)

    def test_add_book_authorized(self):
        # Set up a superuser
        password = 'mypassword'
        superuser = User.objects.create_superuser(
            'superuser',
            'myemail@test.com',
            password
        )
        self.client.login(username=superuser.username, password=password)

        response = self.client.post('/books/add/', {'title': 'Test Book'})
        self.assertEqual(response.status_code, 201)
        self.assertTemplateUsed((response, 'books/add_book.html'))

    def test_delete_book_unauthorized(self):
        book = Book.objects.create(
            title='Test Book'
        )
        response = self.client.get(f'/books/delete/{book.id}')
        self.assertEqual(response.status_code, 401)

    def test_delete_book_authorized(self):
        #  Set up a superuser
        password = 'mypassword'
        superuser = User.objects.create_superuser(
            'superuser',
            'myemail@test.com',
            password
        )
        self.client.login(username=superuser.username, password=password)

        book = Book.objects.create(
            title='Test Book'
        )
        response = self.client.get(f'/books/delete/{book.id}')
        self.assertTemplateUsed((response, 'books/add_book.html'))
        response = self.client.get('/books/delete/{id}')
        self.assertEqual(response.status_code, 200)

    def test_all_stock_unauthorized(self):
        response = self.client.get('/books/all_stock/')
        self.assertEqual(response.status_code, 401)
        self.assertTemplateUsed(response, 'inventory/all_stock.html')

    def test_all_stock_authorized(self):
        #  Set up a superuser
        password = 'mypassword'
        superuser = User.objects.create_superuser(
            'superuser',
            'myemail@test.com',
            password
        )
        self.client.login(username=superuser.username, password=password)

        response = self.client.get('/books/all_stock/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/all_stock.html')

    def test_update_stock_unauthorised(self):
        book = Book.objects.create(
            title='Test Book'
        )
        stock = Stock.objects.create(
            book=book,
            price=1,
            condition='fair',
            quantity=2
        )
        response = self.client.get(f'/books/update_stock/{stock.id}')
        self.assertEqual(response.status_code, 401)
        self.assertTemplateUsed(response, 'inventory/update_stock/{id}')

    def test_update_stock_authorised(self):
        #  Set up a superuser
        password = 'mypassword'
        superuser = User.objects.create_superuser(
            'superuser',
            'myemail@test.com',
            password
        )
        self.client.login(username=superuser.username, password=password)
        book = Book.objects.create(
            title='Test Book'
        )
        stock = Stock.objects.create(
            book=book,
            price=1,
            condition='fair',
            quantity=2
        )
        response = self.client.get(f'/books/update_stock/{stock.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'inventory/update_stock/{stock.id}')
