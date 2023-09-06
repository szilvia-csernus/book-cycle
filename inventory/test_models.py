from django.test import TestCase
from .models import YearGroup, Subject, Book


class TestModels(TestCase):

    def test_yeargroup_string_representation(self):
        year_group = YearGroup(name="Test YearGroup Name")
        self.assertEqual(str(year_group), year_group.name)

    def test_subject_string_representation(self):
        subject = Subject(name="Test Subject Name")
        self.assertEqual(str(subject), subject.name)

    def test_book_string_representation(self):
        book = Book.objects.create(title="Test Book Title")
        self.assertEqual(str(book), book.title)

    def test_slug_field_not_null(self):
        book = Book.objects.create(title="Test Book Title")
        self.assertIsNotNone(book.slug)

    def test_slug_field_is_unique(self):
        book1 = Book.objects.create(title="Test Book Title")
        book2 = Book.objects.create(title="Test Book Title")
        self.assertFalse(book1.slug == book2.slug)
