from django.test import TestCase, Client
from datetime import date
from django.core.exceptions import ValidationError
from .models import Book, Author, Language
from google_books.utils.views_utils import (filter_books,
                                            get_author_object,
                                            get_language_object,
                                            )
from google_books.utils.models_utils import (validate_year,
                                             validate_month,
                                             validate_day,
                                             )


class ValidateYearTestCase(TestCase):

    def test_validate_year_1584(self):
        self.assertTrue(validate_year(1584))

    def test_validate_year_0(self):
        self.assertTrue(validate_year(1))

    def test_validate_year_minus_1(self):
        with self.assertRaises(ValidationError):
            validate_year(-1)

    def test_validate_year_current_year(self):
        self.assertTrue(validate_year(date.today().year))

    def test_validate_year_future_year(self):
        with self.assertRaises(ValidationError):
            validate_year(date.today().year + 1)

    def test_validate_year_None(self):
        self.assertTrue(validate_year(None))


class ValidateMonthTestCase(TestCase):

    def test_validate_month_1_to_12(self):
        for i in range(1, 13):
            with self.subTest(i=i):
                self.assertTrue(validate_month(i))

    def test_validate_month_0(self):
        with self.assertRaises(ValidationError):
            validate_month(0)

    def test_validate_month_13(self):
        with self.assertRaises(ValidationError):
            validate_month(13)

    def test_validate_month_None(self):
        self.assertTrue(validate_month(None))


class ValidateDayTestCase(TestCase):

    def test_validate_day_1_to_31(self):
        for i in range(1, 32):
            with self.subTest(i=i):
                self.assertTrue(validate_day(i))

    def test_validate_month_0(self):
        with self.assertRaises(ValidationError):
            validate_day(0)

    def test_validate_day_32(self):
        with self.assertRaises(ValidationError):
            validate_day(32)

    def test_validate_day_None(self):
        self.assertTrue(validate_day(None))


class FilterBooksTestCase(TestCase):

    def setUp(self):
        language_1 = Language.objects.create(language='pl')
        author_1 = Author.objects.create(name='Adam Mickiewicz')
        book_1 = Book.objects.create(title='Pan Tadeusz', publishedYear=1844, publishedMonth=None, publishedDay=None,
                                     language=language_1, pages=395, cover=None, isbn_10=None, isbn_13=None)
        book_1.authors.set([author_1])
        language_2 = Language.objects.create(language='en')
        author_2 = Author.objects.create(name='Arthur Conan Doyle')
        book_2 = Book.objects.create(title='A Study in Scarlet', publishedYear=1887, publishedMonth=None,
                                     publishedDay=None, language=language_2, pages=183, cover=None, isbn_10=None,
                                     isbn_13=None)
        book_2.authors.set([author_2])
        book_3 = Book.objects.create(title='The Hound of the Baskervilles', publishedYear=1902, publishedMonth=None,
                                     publishedDay=None, language=language_2, pages=235, cover=None, isbn_10=None,
                                     isbn_13=None)
        book_3.authors.set([author_2])

    def test_filter_books_pan(self):
        c = Client()
        response = c.get('/books?title=pan')
        request = response.wsgi_request
        filtered_books = filter_books(request)
        self.assertEqual(len(filtered_books), 1)
        self.assertEqual(filtered_books[0].title, 'Pan Tadeusz')
        self.assertEqual(filtered_books[0].authors.all()[0].name, 'Adam Mickiewicz')

    def test_filter_books_en(self):
        c = Client()
        response = c.get('/books?language=en')
        request = response.wsgi_request
        filtered_books = filter_books(request)
        self.assertEqual(len(filtered_books), 2)
        for book in filtered_books:
            with self.subTest(book=book):
                self.assertEqual(book.language.language, 'en')

    def test_filter_books_en_pan(self):
        c = Client()
        response = c.get('/books?language=en&title=pan')
        request = response.wsgi_request
        filtered_books = filter_books(request)
        self.assertEqual(len(filtered_books), 0)

    def test_filter_books_en_basker(self):
        c = Client()
        response = c.get('/books?language=en&title=basker')
        request = response.wsgi_request
        filtered_books = filter_books(request)
        self.assertEqual(len(filtered_books), 1)
        self.assertEqual(filtered_books[0].language.language, 'en')
        self.assertEqual(filtered_books[0].title, 'The Hound of the Baskervilles')


class GetAuthorObjectTestCase(TestCase):

    def setUp(self):
        Author.objects.create(name='Adam Mickiewicz')

    def test_get_author_object_existing(self):
        author = get_author_object('adam mickiewicz')
        self.assertEqual(author.name, 'Adam Mickiewicz')

    def test_get_author_object_not_existing(self):
        author = get_author_object('Alfred Szklarski')
        self.assertEqual(author.name, 'Alfred Szklarski')


class GetLanguageObjectTestCase(TestCase):

    def setUp(self):
        Language.objects.create(language='en')

    def test_get_language_object_existing(self):
        language = get_language_object('EN')
        self.assertEqual(language.language, 'en')

    def test_get_language_object_not_existing(self):
        language = get_language_object('fr')
        self.assertEqual(language.language, 'fr')


class GetBooksFromApiTestCase(TestCase):

    def test_get_books_from_api(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 302)


class AllBooksViewTestCase(TestCase):

    def test_all_books_view(self):
        c = Client()
        response = c.get('/books/')
        self.assertEqual(response.status_code, 200)


class AddBookViewTestCase(TestCase):

    def setUp(self):
        Author.objects.create(name='new author')
        Author.objects.create(name='another author')

    def test_add_book_view_get(self):
        c = Client()
        response = c.get('/add-book/')
        self.assertEqual(response.status_code, 200)

    def test_add_book_view_post(self):
        authors = Author.objects.all()
        c = Client()
        response = c.post('/add-book/',
                          {'title': 'some title', 'authors': [authors[0].id, authors[1].id], 'publishedYear': '',
                           'publishedMonth': '', 'publishedDay': '', 'isbn_10': '', 'isbn_13': '', 'pages': '',
                           'cover': '', 'language': ''})
        self.assertEqual(response.status_code, 302)

    def test_add_book_view_post_wrong_data(self):
        c = Client()
        response = c.post('/add-book/',
                          {'title': '', 'authors': [], 'publishedYear': '',
                           'publishedMonth': '', 'publishedDay': '', 'isbn_10': '', 'isbn_13': '', 'pages': '',
                           'cover': '', 'language': ''})
        self.assertEqual(response.status_code, 200)
