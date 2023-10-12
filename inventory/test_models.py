from django.test import TestCase
from .models import YearGroup, Subject, Book
from django.urls import reverse


class YearGroupModelTest(TestCase):

    def test_string_representation(self):
        # Create a YearGroup instance and test its string representation
        YearGroup.objects.create(name="alevel", friendly_name="A Level")
        year_group = YearGroup.objects.get(id=1)
        self.assertEqual(str(year_group), "alevel")
        self.assertEqual(str(year_group.friendly_name), "A Level")


class SubjectModelTest(TestCase):

    def test_string_representation(self):
        # Create a Subject instance and test its string representation
        Subject.objects.create(name="computing",
                               friendly_name="Computer Science")
        subject = Subject.objects.get(id=1)
        self.assertEqual(str(subject), "computing")
        self.assertEqual(str(subject.friendly_name), "Computer Science")


class BookModelTest(TestCase):

    def setUp(self):
        # Set up test data for YearGroup and Subject and a Book
        year_group = YearGroup.objects.create(name="alevel")
        subject = Subject.objects.create(name="computing")
        Book.objects.create(
            title="Computer Science for A Level Students",
            year_group=year_group,
            subject=subject,
            image_url="http://example.com/computing.jpg",
            product_url="http://example.com/computing",
        )

    def test_slug_creation(self):
        book = Book.objects.get(id=1)
        # The 'save' method should automatically generate a slug
        self.assertTrue(book.slug)

    def test_get_slug_url(self):
        book = Book.objects.get(id=1)
        # The get_slug_url method should return the full url for the book,
        # when the slug is appended to the 'book_detail' url
        url = reverse("book_detail", kwargs={"slug": book.slug})
        self.assertEqual(book.get_slug_url(), url)

    def test_delete_book(self):
        book = Book.objects.get(id=1)
        # Delete the only book in the database
        book.delete()
        self.assertEqual(Book.objects.count(), 0)
