from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import YearGroup, Subject, Book, Stock
from .forms import BookForm


class InventoryManagementTest(TestCase):

    # Set up test data for all tests below
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
            condition="new",
            quantity=10,
            blocked=2
        )
        Stock.objects.create(
            book=book,
            price=8.00,
            condition="good",
            quantity=10,
            blocked=2
        )
        Stock.objects.create(
            book=book,
            price=3.00,
            condition="fair",
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

    # Test cases for add_book

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
        response = self.client.get(reverse('add_book'))
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

    # Test cases for edit_book

    def test_edit_book_form_rendering_unauthenticated(self):
        book = Book.objects.get(id=1)
        # Test if a non-logged-in user can access the edit_book view
        response = self.client.get(reverse('edit_book',
                                           args=[book.slug]))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'inventory/edit_book.html')

    def test_edit_book_form_rendering_unauthorised(self):
        book = Book.objects.get(id=1)
        # Test if a non-staff user can access the edit_book view
        self.client.login(username='emily', password='emilyspassword')
        response = self.client.get(reverse('edit_book',
                                           args=[book.slug]))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'inventory/edit_book.html')

    def test_edit_book_form_rendering_authorised(self):
        book = Book.objects.get(id=1)
        # Test if a staff member can access the edit_book view
        self.client.login(username='staffmember', password='staffpassword')
        response = self.client.get(reverse('edit_book',
                                           args=[book.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_book.html')
        self.assertIsInstance(response.context['bookform'], BookForm)

    def test_edit_book_form_submission(self):
        book = Book.objects.get(id=1)
        # Test the edit book form's submission
        self.client.login(username='staffmember', password='staffpassword')
        response = self.client.get(reverse('edit_book',
                                           kwargs={'slug': book.slug}))
        price_new = 20.00  # Changed
        price_good = 10.00  # Changed
        price_fair = 3.00  # Changed
        response = self.client.post(
            reverse('edit_book', kwargs={'slug': book.slug}),
            {
                'title': 'Cooking - Food technology',  # Changed
                'stock_new_price': price_new,
                'stock_good_price': price_good,
                'stock_fair_price': price_fair,
            }
        )
        self.assertRaisesMessage(response, 'Successfully updated book!')

    # Test cases for delete_book

    def test_delete_book_unauthorised(self):
        book = Book.objects.get(id=1)
        # Test if a non-staff user can access the delete_book view
        response = self.client.get(reverse('delete_book',
                                           args=[book.slug]))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'inventory/delete_book.html')

    def test_delete_book_submission(self):
        book = Book.objects.get(id=1)
        # Test the delete book form's submission
        self.client.login(username='staffmember', password='staffpassword')
        response = self.client.get(reverse('delete_book',
                                           args=[book.slug]))
        self.assertRaisesMessage(response, 'Book deleted!')

    # Test cases for manage_stock

    def test_manage_stock_unauthorised(self):
        book = Book.objects.get(id=1)
        # Test if a non-staff user can access the manage_stock view
        response = self.client.get(reverse('manage_stock',
                                           args=[book.slug]))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'inventory/manage_stock.html')

    def test_manage_stock_authorised(self):
        book = Book.objects.get(id=1)
        # Test if a staff member can access the manage_stock view
        self.client.login(username='staffmember', password='staffpassword')
        response = self.client.get(reverse('manage_stock',
                                           args=[book.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/manage_stock.html')
        self.assertIsInstance(response.context['book'], Book)
        self.assertEqual(response.context['book'], book)

    # Test cases for add_stock

    def test_add_stock_unauthorised(self):
        stock = Stock.objects.get(id=1)
        # Test if a non-staff user can access the add_stock view
        response = self.client.get(reverse('add_stock',
                                           args=[stock.id]))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'inventory/add_stock.html')

    def test_add_stock_view_successful(self):
        # Test the add_stock view with a valid form submission
        self.client.login(username='staffmember', password='staffpassword')
        stock = Stock.objects.get(id=1)
        response = self.client.post(
            reverse('add_stock', args=[1]),
            {'quantity': 5, 'redirect_url': reverse('manage_stock',
                                                    args=[stock.book.slug])}
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success
        updated_stock = Stock.objects.get(id=1)
        self.assertEqual(updated_stock.quantity, 15)
        self.assertRaisesMessage(response, 'Successfully added stock!')

    def test_add_stock_view_failed(self):
        # Test the add_stock view with an invalid form submission
        self.client.login(username='staffmember', password='staffpassword')
        stock = Stock.objects.get(id=1)
        response = self.client.post(
            reverse('add_stock', args=[1]),
            {'quantity': 'invalid',
             'redirect_url': reverse('manage_stock',
                                     args=[stock.book.slug])}
        )
        self.assertEqual(response.status_code, 302)  # Redirects on failure
        updated_stock = Stock.objects.get(id=stock.id)
        self.assertEqual(updated_stock.quantity, 10)  # Quantity remains
        self.assertRaisesMessage(response, 'Failed to add stock!')
