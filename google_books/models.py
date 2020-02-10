from django.db import models


# Create your models here.
class Book:
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Author')
    publishedDate = models.DateField()
    isbn_10 = models.IntegerField()
    isbn_13 = models.IntegerField()
    pages = models.IntegerField()
    cover = models.URLField()
    language = models.CharField(max_length=64)


class Author:
    names = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
