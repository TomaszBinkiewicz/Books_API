from django.shortcuts import get_object_or_404
from django.http import Http404
from google_books.models import Book, Author, Language


def filter_books(request):
    title = request.GET.get('title')
    author = request.GET.get('author')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    language = request.GET.get('language')
    books = Book.objects.all().order_by('title')
    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(authors__name__icontains=author)
    if year_from:
        books = books.filter(publishedYear__gte=year_from)
    if year_to:
        books = books.filter(publishedYear__lte=year_to)
    if language:
        books = books.filter(language__language__icontains=language)
    return books


def get_author_object(name):
    try:
        author = get_object_or_404(Author, name__iexact=name)
    except Http404:
        author = Author.objects.create(name=name)
    return author


def get_language_object(language):
    try:
        language = get_object_or_404(Language, language__iexact=language)
    except Http404:
        language = Language.objects.create(language=language)
    return language
