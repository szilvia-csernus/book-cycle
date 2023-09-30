from django import forms
from .widgets import CustomClearableFileInput
from .models import YearGroup, Subject, Book, Stock


class BookForm(forms.ModelForm):
    """ Form to add and edit books"""

    stock_new_price = forms.DecimalField(max_digits=6, decimal_places=2,
                                         label='Price (condition: New)')
    stock_good_price = forms.DecimalField(max_digits=6, decimal_places=2,
                                          label='Price (condition: Good)')
    stock_fair_price = forms.DecimalField(max_digits=6, decimal_places=2,
                                          label='Price (condition: Fair)')

    class Meta:
        model = Book
        exclude = ('image_url', 'product_url', 'slug',)

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        year_groups = YearGroup.objects.all()
        subjects = Subject.objects.all()
        friendly_names = [(c.id, c.friendly_name) for c in year_groups]
        friendly_names2 = [(c.id, c.friendly_name) for c in subjects]

        self.fields['year_group'].choices = [('', 'Select Year Group')]\
            + friendly_names
        self.fields['subject'].choices = [('', 'Select Subject')]\
            + friendly_names2
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'stripe-style-input'


class StockForm(forms.ModelForm):
    """ Form to add and edit stock"""
    class Meta:
        model = Stock
        fields = ('price',)
