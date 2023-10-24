from django.test import TestCase
from django.contrib.auth.models import User
from profiles.forms import UserProfileForm


class UserProfileFormTest(TestCase):
    """ Test UserProfileForm """
    def setUp(self):
        # Set up test data
        self.user = User.objects.create_user(username='emily',
                                             password='emilyspassword')
        self.user_profile = self.user.userprofile

    def test_user_profile_form_valid_data(self):
        # Test the form with valid data
        form_data = {
            'default_phone_number': '1234567890',
            'default_country': 'GB',
            'default_postcode': '12345',
            'default_town_or_city': 'City',
            'default_street_address1': 'asdfg',
            'default_street_address2': '',
            'default_county': '',
        }
        form = UserProfileForm(data=form_data, instance=self.user_profile)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_default_country(self):
        # Test the default country is set to 'GB'
        form = UserProfileForm(instance=self.user_profile)
        self.assertEqual(form.initial['default_country'], 'GB')

    def test_user_profile_form_placeholder_and_classes(self):
        # Test the placeholders and classes are correct
        form = UserProfileForm(instance=self.user_profile)
        self.assertEqual(
            form.fields['default_phone_number'].widget.attrs['placeholder'],
            'Phone Number')
        self.assertEqual(
            form.fields['default_phone_number'].widget.attrs['class'],
            'account-form-input')
        self.assertEqual(
            form.fields['default_postcode'].widget.attrs['placeholder'],
            'Postcode')
        self.assertEqual(
            form.fields['default_postcode'].widget.attrs['class'],
            'account-form-input')
        self.assertEqual(
            form.fields['default_town_or_city'].widget.attrs['placeholder'],
            'Town or City')
        self.assertEqual(
            form.fields['default_town_or_city'].widget.attrs['class'],
            'account-form-input')
        self.assertEqual(
            form.fields['default_street_address1'].widget.attrs['placeholder'],
            '1st Line of Address')
        self.assertEqual(
            form.fields['default_street_address1'].widget.attrs['class'],
            'account-form-input')
        self.assertEqual(
            form.fields['default_street_address2'].widget.attrs['placeholder'],
            '2nd Line of Address')
        self.assertEqual(
            form.fields['default_street_address2'].widget.attrs['class'],
            'account-form-input')
        self.assertEqual(
            form.fields['default_county'].widget.attrs['placeholder'],
            'County')

    def test_user_profile_form_labels(self):
        # Test the labels are correct
        form = UserProfileForm(instance=self.user_profile)
        self.assertEqual(form.fields['default_phone_number'].label,
                         'Phone Number')
        self.assertEqual(form.fields['default_postcode'].label, 'Postcode')
        self.assertEqual(form.fields['default_town_or_city'].label,
                         'Town or City')
        self.assertEqual(form.fields['default_street_address1'].label,
                         '1st Line of Address')
        self.assertEqual(form.fields['default_street_address2'].label,
                         '2nd Line of Address')
        self.assertEqual(form.fields['default_county'].label, 'County')
