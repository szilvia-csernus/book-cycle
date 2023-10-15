from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from inventory.models import YearGroup, Subject, Book, Stock
from orders.models import Order, OrderLineItem


class CheckoutViewTest(TestCase):
    def setUp(self):
        # Set up test data inclluding adding items to the shopping bag
        year_group = YearGroup.objects.create(name="alevel")
        subject = Subject.objects.create(name="computing")

        # Create a test image
        image_path = "testing_files/img_for_testing_img_upload.png"
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
        self.mock_image = SimpleUploadedFile("test_image.png",
                                             image_content,
                                             content_type="image/png")

        book = Book.objects.create(
            title="Computer Science",
            year_group=year_group,
            subject=subject,
            image=self.mock_image
        )

        self.stock = Stock.objects.create(
            book=book,
            condition="new",
            price=10.00,
            quantity=10
        )

        # Create a simple user (not staff)
        User.objects.create_user(
            username='emily',
            password='emilyspassword',
            is_staff=False
        )

        self.session = self.client.session
        self.session['bag'] = {str(self.stock.id): 3}
        self.session.save()

    def test_checkout_view_get(self):
        # Test the checkout view for GET request
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout.html')

    def test_checkout_view_get_authenticated(self):
        # Test the checkout view for GET request when shopper is signed in
        self.client.login(username='emily', password='emilyspassword')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout.html')

    def test_checkout_view_post_with_postage(self):
        # Test the checkout view for POST request when user selects postage
        response = self.client.post(reverse('checkout'), {
            'shipping-info': 'post',
            'full_name': 'Emily Grant',
            'email': 'emilygrant@example.com',
            'phone_number': '1234567890',
            'country': 'GB',
            'postcode': '12345',
            'town_or_city': 'City',
            'street_address1': 'asasdfdf',
            'street_address2': '',
            'county': '',
            'client_secret': '111111_secret_111111',
        })

        # Check that the order was created
        orders = Order.objects.filter(email='emilygrant@example.com')
        self.assertEqual(orders.count(), 1)
        order = orders.first()
        self.assertEqual(order.full_name, 'Emily Grant')

        # Expecting a redirection to the 'update_stock' view
        self.assertEqual(response.status_code, 302)

    def test_checkout_view_post_with_collection(self):
        # Test the checkout view for POST request when user selects collection
        response = self.client.post(reverse('checkout'), {
            'shipping-info': 'pickup',
            'full_name': 'Emily Grant',
            'email': 'emilygrant@example.com',
            'phone_number': '1234567890',
            'country': 'GB',
            'postcode': '12345',
            'town_or_city': '',
            'street_address1': '',
            'street_address2': '',
            'county': '',
            'client_secret': '111111_secret_111111',
        })

        # Check that the order was created
        orders = Order.objects.filter(email='emilygrant@example.com')
        self.assertEqual(orders.count(), 1)
        order = orders.first()
        self.assertEqual(order.full_name, 'Emily Grant')

        # Expecting a redirection to the 'update_stock' view
        self.assertEqual(response.status_code, 302)

    def test_checkout_view_with_no_items_in_bag(self):
        # Test the checkout view with no items in the bag
        # We have to remove the items from the shopping bag first
        self.session = self.client.session
        self.session['bag'] = {}
        self.session.save()

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        # Expecting a redirect to the books page
        self.assertRedirects(response, reverse('books'))

    def test_check_stock_and_update_bag_with_enough_stock(self):
        # Test the check_stock_and_update_bag view when there is enough stock
        response = self.client.get(reverse('check_stock_and_update_bag'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('checkout'))

    def test_check_stock_and_update_bag_with_insufficient_stock(self):
        # Test the check_stock_and_update_bag view when stock is not enough
        self.session['bag'] = {str(self.stock.id): 11}
        self.session.save()
        response = self.client.get(reverse('check_stock_and_update_bag'))
        self.assertEqual(response.status_code, 302)
        # Expecting a redirect to the shopping bag page
        self.assertRedirects(response,
                             reverse('view_bag'))

    def test_update_stock(self):
        # Test the update_stock view
        # Create a new order
        order = Order.objects.create(
            full_name='Emily Grant',
            email='emilygrant@example.com',
            phone_number='1234567890',
            country='GB',
            postcode='12345',
            shipping_required=False,
        )
        # Add a line item to the order
        OrderLineItem.objects.create(
            order=order,
            stock=self.stock,
            quantity=2,
        )
        self.stock.blocked = 2
        self.stock.save()

        response = self.client.get(reverse('update_stock',
                                           args=[order.order_number]))
        self.assertEqual(response.status_code, 302)
        # Expecting the stock to be reduced by 2
        self.assertEqual(self.stock.quantity, 8)
