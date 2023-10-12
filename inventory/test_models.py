from django.test import TestCase
from .models import YearGroup, Subject


class YearGroupModelTest(TestCase):

    def test_string_representation(self):
        YearGroup.objects.create(name="alevel", friendly_name="A Level")
        year_group = YearGroup.objects.get(id=1)
        self.assertEqual(str(year_group), "alevel")
        self.assertEqual(str(year_group.friendly_name), "A Level")


class SubjectModelTest(TestCase):

    def test_string_representation(self):
        Subject.objects.create(name="computing",
                               friendly_name="Computer Science")
        subject = Subject.objects.get(id=1)
        self.assertEqual(str(subject), "computing")
        self.assertEqual(str(subject.friendly_name), "Computer Science")
