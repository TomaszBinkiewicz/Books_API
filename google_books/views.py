from django.shortcuts import render, get_object_or_404, redirect
import requests
from django.http import HttpResponse, Http404
from .models import Book
from datetime import datetime
from django.views import View
from .forms import AddBookForm, ImportFromApiForm
from django.core.paginator import Paginator
from google_books.utils.views_utils import (filter_books,
                                            get_language_object,
                                            get_author_object,
                                            )


def get_books_from_api(request, url='https://www.googleapis.com/books/v1/volumes?q=Hobbit'):
    """
    Acquire data from google api and save new records to database
    """
    response = requests.get(url)
    data = response.json()
    items = data.get('items')
    if items is None:
        items = []
    for item in items:
        book = item.get('volumeInfo')
        title = book.get('title', '--')
        authors = book.get('authors', ['unknown'])
        publishedDate = book.get('publishedDate')
        isbns = book.get('industryIdentifiers', [])
        pages = book.get('pageCount')
        cover_url = book.get('imageLinks')
        if cover_url:
            cover_url = cover_url.get('thumbnail')
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
        except TypeError:
            year = None
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
    return redirect('all-books')


class AllBooksView(View):
    def get(self, request):
        all_books = filter_books(request)
        paginator = Paginator(all_books, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'google_books/all_books.html', context={'books': page_obj})


class AddBookView(View):
    def get(self, request):
        form = AddBookForm()
        return render(request, 'google_books/base_form.html', context={'form': form, 'submit': 'ADD'})

    def post(self, request):
        form = AddBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            authors = form.cleaned_data.get('authors')
            published_year = form.cleaned_data.get('publishedYear')
            published_month = form.cleaned_data.get('publishedMonth')
            published_day = form.cleaned_data.get('publishedDay')
            isbn_10 = form.cleaned_data.get('isbn_10')
            isbn_13 = form.cleaned_data.get('isbn_13')
            pages = form.cleaned_data.get('pages')
            cover = form.cleaned_data.get('cover')
            language = form.cleaned_data.get('language')
            new_book = Book.objects.create(title=title, publishedYear=published_year, publishedDay=published_day,
                                           publishedMonth=published_month, isbn_10=isbn_10, isbn_13=isbn_13,
                                           pages=pages, cover=cover, language=language)
            for author in authors:
                new_book.authors.add(author)
            return redirect('all-books')
        else:
            return render(request, 'google_books/base_form.html', context={'form': form, 'submit': 'ADD'})


class ImportFromApiView(View):
    def get(self, request):
        form = ImportFromApiForm()
        return render(request, 'google_books/base_form.html', context={'form': form, 'submit': 'Import'})

    def post(self, request):
        url = 'https://www.googleapis.com/books/v1/volumes?q='
        form = ImportFromApiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            publisher = form.cleaned_data.get('publisher')
            subject = form.cleaned_data.get('subject')
            isbn = form.cleaned_data.get('isbn')
            lccn = form.cleaned_data.get('lccn')
            oclc = form.cleaned_data.get('oclc')
            if title:
                url += f'+intitle:{title}'
            if author:
                url += f'+inauthor:{author}'
            if publisher:
                url += f'+inpublisher:{publisher}'
            if subject:
                url += f'+subject:{subject}'
            if isbn:
                url += f'+isbn:{isbn}'
            if lccn:
                url += f'+lccn:{lccn}'
            if oclc:
                url += f'+intitle:{oclc}'
            print(url)
            get_books_from_api(request, url=url)
            return redirect('all-books')
        else:
            return render(request, 'google_books/base_form.html', context={'form': form, 'submit': 'Import'})
