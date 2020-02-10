from django.shortcuts import render, get_object_or_404
import requests
from django.http import HttpResponse, Http404
from .models import Book, Author, Language
from datetime import datetime
from django.views import View


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


def get_books_from_api(request):
    """
    Acquire data from google api (https://www.googleapis.com/books/v1/volumes?q=Hobbit) and save new records to database
    """
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit')
    data = response.json()
    ret_str = ''
    for item in data['items']:
        book = item.get('volumeInfo')
        ret_str += f"""{book.get('title')}, {book.get('authors')}, {book.get('publishedDate')},
              {book.get('industryIdentifiers')}, {book.get('pageCount')},
              {book.get('imageLinks').get('thumbnail')}, {book.get('language')}<br><br>"""
        title = book.get('title')
        authors = book.get('authors')
        publishedDate = book.get('publishedDate')
        isbns = book.get('industryIdentifiers')
        pages = book.get('pageCount')
        cover_url = book.get('imageLinks').get('thumbnail')
        language = book.get('language')
        authors_list = []
        for author in authors:
            auth = get_author_object(author)
            authors_list.append(auth)
        isbn_10 = None
        isbn_13 = None
        for isbn in isbns:
            if isbn['type'] == 'ISBN_10':
                isbn_10 = isbn['identifier']
            elif isbn['type'] == 'ISBN_13':
                isbn_13 = isbn['identifier']
        lang = get_language_object(language)
        try:
            published = datetime.strptime(publishedDate, '%Y-%m-%d')
        except ValueError:
            year = int(publishedDate[:4])
            month = None
            day = None
        else:
            year = published.year
            month = published.month
            day = published.day
        try:
            book = get_object_or_404(Book, title=title, publishedYear=year, publishedMonth=month, publishedDay=day,
                                     language=lang, pages=pages, cover=cover_url, isbn_10=isbn_10, isbn_13=isbn_13)
            for name in book.authors.all():
                if name not in authors_list:
                    raise Http404
        except Http404:
            book = Book.objects.create(title=title, publishedYear=year, publishedMonth=month, publishedDay=day,
                                       language=lang, pages=pages, cover=cover_url, isbn_10=isbn_10, isbn_13=isbn_13)
            book.authors.set(authors_list)
    return HttpResponse(ret_str)


class AllBooksView(View):
    def get(self, request):
        all_books = Book.objects.all().order_by('title')
        return render(request, 'google_books/all_books.html', context={'books': all_books})
