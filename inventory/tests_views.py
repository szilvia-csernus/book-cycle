from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Stock


def create_and_login_superuser(self):
    password = 'mypassword'
    superuser = User.objects.create_superuser(
        'superuser',
        'myemail@test.com',
        password
    )
    self.client.login(username=superuser.username, password=password)


def create_a_book():
    book = Book.objects.create(
            title='Test Book'
        )
    return book


class TestViews(TestCase):

    def test_all_books(self):
        response = self.client.get('/inventory/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/books.html')

    def test_book_detail(self):
        create_and_login_superuser(self)
        book = create_a_book()
        response = self.client.get(f'/inventory/books/{book.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'inventory/book/{book.slug}')

    def test_add_book_unauthorized(self):
        response = self.client.post('/books/add/', {'title': 'Test Book'})
        self.assertEqual(response.status_code, 401)

    def test_add_book_authorized(self):
        create_and_login_superuser(self)

        response = self.client.post('/books/add/', {'title': 'Test Book'})
        self.assertEqual(response.status_code, 201)
        self.assertRedirects((response, 'books/'))

    def test_delete_book_unauthorized(self):
        book = create_a_book()
        response = self.client.get(f'/books/delete/{book.id}')
        self.assertEqual(response.status_code, 401)

    def test_delete_book_authorized(self):
        create_and_login_superuser(self)

        book = create_a_book()
        response = self.client.get(f'/books/delete/{book.id}')
        self.assertRedirects(response, 'books/')
        book_in_database = Book.objects.filter(id=book.id)
        self.assertEqual(len(book_in_database), 0)

    def test_all_stock_unauthorized(self):
        response = self.client.get('/books/all_stock/')
        self.assertEqual(response.status_code, 401)

    def test_all_stock_authorized(self):
        create_and_login_superuser(self)

        response = self.client.get('/books/all_stock/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/all_stock.html')

    def test_update_stock_unauthorised(self):
        book = create_a_book()
        stock = Stock.objects.create(
            book=book,
            price=1,
            condition='fair',
            quantity=2
        )
        response = self.client.post(f'/books/update_stock/{stock}')
        self.assertEqual(response.status_code, 401)
        self.assertTemplateUsed(response, f'inventory/edit_stock/{stock.id}')

    def test_update_stock_authorised(self):
        create_and_login_superuser(self)
        book = create_a_book()
        stock = Stock.objects.create(
            book=book,
            price=1,
            condition='fair',
            quantity=2
        )
        response = self.client.post(f'/books/update_stock/{stock}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'inventory/edit_stock/{stock.id}')
