from django import forms
from .models import validate_year, validate_month, validate_day, Author, Language
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


def validate_positive_int(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s cannot be a proper value'),
            params={'value': value},
        )


class AddBookForm(forms.Form):
    value_error = {
        'required': 'This field is required',
        'invalid': 'Invalid',
        'invalid_choice': 'No such value'
    }
    title = forms.CharField(max_length=64, label='Title')
    authors = forms.ModelChoiceField(label='First name', queryset=Author.objects.all(), error_messages=value_error)
    publishedYear = forms.IntegerField(label='Year of publication', validators=[validate_year], required=False)
    publishedMonth = forms.IntegerField(label='Month of publication', validators=[validate_month], required=False)
    publishedDay = forms.IntegerField(label='Day of publication', validators=[validate_day], required=False)
    isbn_10 = forms.CharField(label='ISBN 10', validators=[validate_isbn_10], required=False)
    isbn_13 = forms.CharField(label='ISBN 13', validators=[validate_isbn_13], required=False)
    pages = forms.IntegerField(label='Number of pages', validators=[validate_positive_int], required=False)
    cover = forms.URLField(label='Book cover url', validators=[URLValidator], required=False)
    language = forms.ModelChoiceField(label='Language', queryset=Language.objects.all(), error_messages=value_error,
                                      required=False)
