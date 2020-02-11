from django import forms
from .models import validate_year, Author, Language
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator


def validate_isbn_10(value):
    value = value.strip()
    not_int = False
    try:
        int(value)
    except ValueError:
        not_int = True
    if not_int or len(value) != 10:
        raise ValidationError(
            _('%(value)s cannot be a proper ISBN_10 number'),
            params={'value': value},
        )


def validate_isbn_13(value):
    value = value.strip()
    not_int = False
    try:
        int(value)
    except ValueError:
        not_int = True
    if not_int or len(value) != 13:
        raise ValidationError(
            _('%(value)s cannot be a proper ISBN_13 number'),
            params={'value': value},
        )


class AddBookForm(forms.Form):
    value_error = {
        'required': 'This field is required',
        'invalid': 'Invalid',
        'invalid_choice': 'No such value'
    }
    title = forms.CharField(max_length=64, label='Title')
    authors = forms.ModelMultipleChoiceField(label='Authors', queryset=Author.objects.all(), error_messages=value_error)
    publishedYear = forms.IntegerField(label='Year of publication', validators=[validate_year], required=False)
    publishedMonth = forms.IntegerField(label='Month of publication', required=False, min_value=1, max_value=12)
    publishedDay = forms.IntegerField(label='Day of publication', required=False, min_value=1, max_value=31)
    isbn_10 = forms.CharField(label='ISBN 10', validators=[validate_isbn_10], required=False)
    isbn_13 = forms.CharField(label='ISBN 13', validators=[validate_isbn_13], required=False)
    pages = forms.IntegerField(label='Number of pages', required=False, min_value=0, max_value=2147483647)
    cover = forms.URLField(label='Book cover url', validators=[URLValidator], required=False)
    language = forms.ModelChoiceField(label='Language', queryset=Language.objects.all(), error_messages=value_error,
                                      required=False)

    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('publishedYear')
        month = cleaned_data.get('publishedMonth')
        day = cleaned_data.get('publishedDay')
        if year is None and (month or day) is not None:
            raise forms.ValidationError('Please select year of publication')
        if day is not None and month is None:
            raise forms.ValidationError('Please select month of publication')