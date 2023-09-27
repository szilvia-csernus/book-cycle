from django import forms
from .models import YearGroup, Subject, Book, Stock


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        year_groups = YearGroup.objects.all()
        subjects = Subject.objects.all()
        friendly_names = [(c.id, c.friendly_name) for c in year_groups]
        friendly_names2 = [(c.id, c.friendly_name) for c in subjects]

        self.fields['year_group'].choices = friendly_names
        self.fields['subject'].choices = friendly_names2
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'stripe-style-input'
