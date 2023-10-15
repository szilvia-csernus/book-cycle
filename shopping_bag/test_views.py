from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from inventory.models import YearGroup, Subject, Stock, Book

import os


class ShoppingBagViewsTest(TestCase):
    def setUp(self):
        year_group = YearGroup.objects.create(name="alevel")
        subject = Subject.objects.create(name="computing")
        # Use a mock image for the book
        image_path = "testing_files/img_for_testing_img_upload.png"
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
        # Get the image file name
        image_name = os.path.basename(image_path)

        # Create a SimpleUploadedFile
        self.mock_image = SimpleUploadedFile(image_name,
                                             image_content,
                                             content_type="image/png")
        book = Book.objects.create(
            title="Computer Science",
            year_group=year_group,
            subject=subject,
            image=self.mock_image
        )
        self.stock_new = Stock.objects.create(
            book=book,
            condition="new",
            price=10.00,
            quantity=10
        )

    def test_view_bag(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_bag/bag.html')

    def test_add_to_bag(self):
        stock_id = self.stock_new.id
        url = reverse('add_to_bag', args=[stock_id])

        # Use the Django test client's session to set and retrieve session data
        session = self.client.session
        session['bag'] = {}
        session.save()

        response = self.client.post(url, {'redirect_url': '/'})

        # Check if the stock was added to the bag
        self.assertIn(str(stock_id), self.client.session['bag'])
        self.assertEqual(self.client.session['bag'][str(stock_id)], 1)
        self.assertRedirects(response, '/')

    def test_remove_from_bag(self):
        stock_id = self.stock_new.id
        url = reverse('remove_from_bag', args=[stock_id])

        # Use the Django test client's session to set and retrieve session data
        session = self.client.session
        session['bag'] = {str(stock_id): 2}
        session.save()

        response = self.client.post(url, {'redirect_url': '/',
                                          'quantity_to_remove': 1})

        # Check if the stock quantity was reduced
        self.assertEqual(self.client.session['bag'][str(stock_id)], 1)
        self.assertRedirects(response, '/')
