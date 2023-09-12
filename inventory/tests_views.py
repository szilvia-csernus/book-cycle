from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Stock, YearGroup, Subject


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


def create_books_with_subject_and_yeargroup(self):
    self.year_group1 = YearGroup.objects.create(name='gcse')
    self.year_group2 = YearGroup.objects.create(name='a-level')
    self.subject1 = Subject.objects.create(name='maths')
    self.subject2 = Subject.objects.create(name='english')

    self.book1 = Book.objects.create(
        title='Test Book 1',
        year_group=self.year_group1,
        subject=self.subject1)
    self.book2 = Book.objects.create(
        title='Test Book 2',
        year_group=self.year_group2,
        subject=self.subject2)
    self.book3 = Book.objects.create(
        title='Test Book 3',
        year_group=self.year_group1,
        subject=self.subject1)


class AllBooksViewTestCase(TestCase):

    def test_all_books(self):
        response = self.client.get('/inventory/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/books.html')

    def test_search_books_with_valid_query(self):
        create_books_with_subject_and_yeargroup(self)
        # Test searching for books with a valid query
        response = self.client.get(
            reverse('books'), {'search': 'Test Book 1'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['books'], ['<Book: Test Book 1>'])

    def test_search_books_with_empty_query(self):
        create_books_with_subject_and_yeargroup(self)
        # Test searching for books with an empty query
        response = self.client.get(reverse('books'), {'search': ''})
        self.assertEqual(response.status_code, 200)

    def test_filter_books_by_year_group(self):
        create_books_with_subject_and_yeargroup(self)
        # Test filtering books by year group
        response = self.client.get(
            reverse('books'), {'year_group': 'a-level'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['books'],
            ['<Book: Test Book 2>'])


class TestBookDetailViews(TestCase):

    def test_book_detail(self):
        create_and_login_superuser(self)
        book = create_a_book()
        response = self.client.get(f'/inventory/books/{book.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/book_detail.html')

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
