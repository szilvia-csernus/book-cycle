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
        book = Book(title="Test Book Title")
        self.assertEqual(str(book), book.title)
