from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import YearGroup, Subject, Book, Stock
from .forms import BookForm


class InventoryManagementTest(TestCase):

    def setUp(self):
        # Create a simple user
        User.objects.create_user(
            username='emily',
            password='emilyspassword',
            is_staff=False
        )
        # Create a user with staff permissions
        User.objects.create_user(
            username='staffmember',
            password='staffpassword',
            is_staff=True
        )
        year_group = YearGroup.objects.create(name="junior")
        subject = Subject.objects.create(name="dance")
        book = Book.objects.create(
            title="Ballet for Juniors",
            year_group=year_group,
            subject=subject,
            exam_board="Dance Exam Board",
            publisher="Any Publisher",
            image_url="http://example.com/ballet.jpg",
            product_url="http://example.com/ballet",
        )
        Stock.objects.create(
            book=book,
            price=10.00,
            condition="New",
            quantity=10,
            blocked=2
        )

    def test_all_books_view(self):
        # Test that the all_books view returns a 200 response
        # and uses the correct template
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/books.html')

    def test_book_detail_view(self):
        book = Book.objects.get(id=1)
        # Test that the book_detail view returns a 200 response
        response = self.client.get(reverse('book_detail',
                                           args=[book.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/book_detail.html')
        # Check that the rendered context contains the book
        self.assertEqual(response.context['book'], book)

    def test_add_book_form_rendering_unauthenticated(self):
        # Test if a non-logged-in user can access the add_book view
        response = self.client.get(reverse('add_book'))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'inventory/add_book.html')

    def test_add_book_form_rendering_unauthorised(self):
        # Test if a non-staff user can access the add_book view
        self.client.login(username='emily', password='emilyspassword')
        response = self.client.get(reverse('add_book'))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'inventory/add_book.html')

    def test_add_book_form_rendering_authorised(self):
        # Test if a staff member can access the add_book view
        self.client.login(username='staffmember', password='staffpassword')
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/add_book.html')
        self.assertIsInstance(response.context['bookform'], BookForm)

    def test_add_book_form_submission(self):
        # Test a valid form submission
        self.client.login(username='staffmember', password='staffpassword')
        yeargroup = YearGroup.objects.get(id=1)
        subject = Subject.objects.get(id=1)
        price_new = 10.00
        price_good = 8.00
        price_fair = 6.00
        response = self.client.post(
            reverse('add_book'),
            {
                'title': 'Cooking',
                'year_group': yeargroup,
                'subject': subject,
                'stock_new_price': price_new,
                'stock_good_price': price_good,
                'stock_fair_price': price_fair,
            }
        )
        self.assertRaisesMessage(response, 'Book added successfully')
