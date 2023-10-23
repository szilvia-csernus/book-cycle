from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """ Form to add order data """
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number', 'country',
                  'postcode', 'street_address1', 'street_address2',
                  'town_or_city', 'county')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
            'street_address1': '1st Line of Address',
            'street_address2': '2nd Line of Address',
            'county': 'County',
        }
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
            'street_address1': '1st Line of Address',
            'street_address2': '2nd Line of Address',
            'county': 'County',
        }

        self.initial['country'] = 'GB'

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = labels[field]


class ShippingForm(forms.Form):
    """ Form to add shipping data"""
    tracking_number = forms.CharField(
        max_length=80,
        required=False,
        label='Tracking Number (optional)',
        widget=forms.TextInput(attrs={'class': 'stripe-style-input'})
    )


class CollectionForm(forms.Form):
    """ Form to add shipping data"""
    collected_by = forms.CharField(
        max_length=80,
        required=True,
        label='Name of person collecting',
        widget=forms.TextInput(attrs={'class': 'stripe-style-input'})
    )
