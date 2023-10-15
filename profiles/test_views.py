from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount

from orders.models import Order, OrderLineItem
from profiles.models import UserProfile
from inventory.models import YearGroup, Subject, Book, Stock


class ProfileViewTest(TestCase):
    def setUp(self):
        # Create a simple user (not staff) and log her in
        self.user = User.objects.create_user(
            username='emily',
            password='emilyspassword',
            is_staff=False
        )
        self.client.login(username='emily',
                          password='emilyspassword')

    def test_profile_view_get(self):
        # Test that user can access the profile page
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['full_name'],
                         self.user.get_full_name())
        self.assertEqual(response.context['form'].instance,
                         self.user.userprofile)
        self.assertEqual(response.context['orders'].count(), 0)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_view_post(self):
        # Test that user can update her profile
        self.client.post(reverse('profile'), {
            'default_phone_number': '9876',
        })
        self.user.userprofile.refresh_from_db()
        # Assert that the user's profile has been updated
        self.assertEqual(self.user.userprofile.default_phone_number, '9876')
        self.assertTemplateUsed('profiles/profile.html')

    def test_order_history(self):
        # Create a year_group, subject, book and a stock
        year_group = YearGroup.objects.create(name="alevel")
        subject = Subject.objects.create(name="computing")
        book = Book.objects.create(
            title="Computer Science",
            year_group=year_group,
            subject=subject,
        )
        self.stock = Stock.objects.create(
            book=book,
            condition="new",
            price=10.00,
            quantity=10
        )
        # Create a new order
        order = Order.objects.create(
            full_name='Emily Grant',
            email='emilygrant@example.com',
            phone_number='1234567890',
            country='GB',
            postcode='12345',
            town_or_city='City',
            street_address1='asdfhgf',
            shipping_required=True
        )
        # Add a line item to the order
        OrderLineItem.objects.create(
            order=order,
            stock=self.stock,
            quantity=2,
        )
        response = self.client.get(reverse('order_history',
                                           args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout_success.html')
        self.assertEqual(response.context['order'], order)
        self.assertEqual(response.context['from_profile'], True)

    def test_delete_profile(self):
        # Test that user can delete her profile
        # Create a social account for the user
        SocialAccount.objects.create(
            user=self.user,
            provider='google',
            uid='12345',
        )
        self.assertTrue(UserProfile.objects.filter(
            user=self.user).exists())
        self.assertTrue(SocialAccount.objects.filter(
            user=self.user).exists())

        # Delete the user's profile
        self.client.post(reverse('delete_profile'))
        # Assert that the user's profile has been deleted
        self.assertFalse(User.objects.filter(
            username='emily').exists())
        self.assertFalse(UserProfile.objects.filter(
            user=self.user).exists())
        self.assertFalse(SocialAccount.objects.filter(
            user=self.user).exists())
