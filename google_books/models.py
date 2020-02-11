from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


def validate_year(value):
    if value is not None and (value < 0 or value > date.today().year):
        raise ValidationError(
            _('%(value)s cannot be a proper year'),
            params={'value': value},
        )


def validate_month(value):
    if value is not None and (value < 1 or value > 12):
        raise ValidationError(
            _('%(value)s not a valid month'),
            params={'value': value},
        )


def validate_day(value):
    if value is not None and (value < 1 or value > 31):
        raise ValidationError(
            _('%(value)s not a valid day'),
            params={'value': value},
        )


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Author')
    publishedYear = models.IntegerField(null=True, validators=[validate_year])
    publishedMonth = models.IntegerField(null=True, validators=[validate_month])
    publishedDay = models.IntegerField(null=True, validators=[validate_day])
    isbn_10 = models.CharField(max_length=10, null=True)
    isbn_13 = models.CharField(max_length=13, null=True)
    pages = models.IntegerField(null=True)
    cover = models.URLField(null=True)
    language = models.ForeignKey('Language', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        auths = self.authors.all()
        authors = ''
        for auth in auths:
            authors += f'{auth}, '
        if self.publishedYear:
            date = str(self.publishedYear)
        else:
            date = '--'
        if self.publishedDay:
            date += f'-{self.publishedMonth}-{self.publishedDay}'
        if self.isbn_10:
            ISBN_10 = self.isbn_10
        else:
            ISBN_10 = '--'
        if self.isbn_13:
            ISBN_13 = self.isbn_13
        else:
            ISBN_13 = '--'
        if self.language:
            language = self.language
        else:
            language = '--'
        if self.pages:
            pages = self.pages
        else:
            pages = '--'
        ret_str = f"""'{self.title}', {authors} published: {date}, language: {language}, pages: {pages},
                    ISBN 10: {ISBN_10}, ISBN 13: {ISBN_13}"""
        return ret_str


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.CharField(max_length=64)

    def __str__(self):
        return self.language
