from django.test import TestCase
from django.contrib.auth import get_user_model
from profiles.models import UserProfile

User = get_user_model()


class UserProfileModelTest(TestCase):
    def test_user_profile_creation(self):
        user = User.objects.create_user(username='emily',
                                        password='emilyspassword')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.user, user)
        self.assertIsNone(profile.default_phone_number)
        self.assertIsNone(profile.default_street_address1)

    def test_user_profile_str_method(self):
        user = User.objects.create_user(username='emily',
                                        password='emilyspassword')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(profile), user.get_full_name())


class UserProfileSignalTest(TestCase):
    def test_create_user_profile_on_user_creation(self):
        user = User.objects.create_user(username='emily',
                                        password='emilyspassword')
        self.assertTrue(hasattr(user, 'userprofile'))
        self.assertEqual(user.userprofile.user, user)

    def test_update_user_profile_on_user_save(self):
        user = User.objects.create_user(username='emily',
                                        password='emilyspassword')
        user.userprofile.default_phone_number = '123456'
        user.userprofile.save()
        updated_user = User.objects.get(username='emily')
        self.assertEqual(updated_user.userprofile.default_phone_number,
                         '123456')
