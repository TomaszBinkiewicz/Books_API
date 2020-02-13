from rest_framework.test import APITestCase
from rest_framework import status
from google_books.models import Book, Author, Language


def create_book():
    author = Author.objects.create(name='J. R. R. Tolkien')
    language = Language.objects.create(language='en')
    book = Book.objects.create(title='A Guide for Using The Hobbit in the Classroom', publishedYear=1992,
                               publishedMonth=None, publishedDay=None, isbn_10='1557344051',
                               isbn_13='9781557344052', pages=48, cover=None, language=language)
    book.authors.set([author])
    return True


def create_multiple_books():
    for _ in range(2):
        create_book()
    return True


class AllLanguagesAPITestCase(APITestCase):

    def test_create_language(self):
        url = '/API/languages'
        data = {'language': 'en'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(Language.objects.get().language, 'en')

    def test_get_language_list(self):
        Language.objects.create(language='en')
        Language.objects.create(language='pl')
        url = '/API/languages'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Language.objects.count(), 2)

    def test_delete_language_list(self):
        Language.objects.create(language='en')
        Language.objects.create(language='pl')
        url = '/API/languages'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Language.objects.count(), 0)


class LanguageAPITestCase(APITestCase):

    def test_display_language(self):
        url = '/API/languages/1'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        Language.objects.create(language='pl')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'language': 'pl'})

    def test_update_language(self):
        Language.objects.create(language='pl')
        url = '/API/languages/1'
        data = {'language': 'en'}
        response = self.client.put(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Language.objects.get().language, 'en')

    def test_delete_language(self):
        Language.objects.create(language='pl')
        url = '/API/languages/1'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Language.objects.count(), 0)


class AllAuthorsAPITestCase(APITestCase):

    def test_create_author(self):
        url = '/API/authors'
        data = {'name': 'Alfred Szklarski'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().name, 'Alfred Szklarski')

    def test_get_authors_list(self):
        Author.objects.create(name='Alfred Szklarski')
        Author.objects.create(name='J. R. R. Tolkien')
        url = '/API/authors'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.count(), 2)

    def test_delete_authors_list(self):
        Author.objects.create(name='Alfred Szklarski')
        Author.objects.create(name='J. R. R. Tolkien')
        url = '/API/authors'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class AuthorAPITestCase(APITestCase):

    def test_display_author(self):
        url = '/API/authors/1'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        Author.objects.create(name='Alfred Szklarski')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'Alfred Szklarski'})

    def test_update_author(self):
        Author.objects.create(name='Alfred Szklarski')
        url = '/API/authors/1'
        data = {'name': 'Alfred Szklarski'}
        response = self.client.put(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.get().name, 'Alfred Szklarski')

    def test_delete_author(self):
        Author.objects.create(name='Alfred Szklarski')
        url = '/API/authors/1'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class AllBooksAPITestCase(APITestCase):

    def test_create_book(self):
        url = '/API/books'
        Author.objects.create(name='Patty Carratello')
        Language.objects.create(language='en')
        data = {'title': 'A Guide for Using The Hobbit in the Classroom',
                'publishedYear': 1992,
                'publishedMonth': None,
                'publishedDay': None,
                'isbn_10': '1557344051',
                'isbn_13': '9781557344052',
                'pages': 48,
                'cover': None,
                'language': 1,
                'authors': [
                    1
                ]}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'A Guide for Using The Hobbit in the Classroom')
        self.assertEqual(Book.objects.get().publishedYear, 1992)
        self.assertEqual(Book.objects.get().publishedMonth, None)
        self.assertEqual(Book.objects.get().publishedDay, None)
        self.assertEqual(Book.objects.get().isbn_10, '1557344051')
        self.assertEqual(Book.objects.get().isbn_13, '9781557344052')
        self.assertEqual(Book.objects.get().pages, 48)
        self.assertEqual(Book.objects.get().cover, None)

    def test_get_books_list(self):
        create_multiple_books()
        url = '/API/books'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_books_list(self):
        create_multiple_books()
        url = '/API/books'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


class BookAPITestCase(APITestCase):

    def test_display_book(self):
        url = '/API/books/1'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        create_book()
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'id': 1, 'title': 'A Guide for Using The Hobbit in the Classroom', 'publishedYear': 1992,
                          'publishedMonth': None, 'publishedDay': None, 'isbn_10': '1557344051',
                          'isbn_13': '9781557344052', 'pages': 48, 'cover': None, 'language': 1, 'authors': [1]})

    def test_update_book(self):
        create_book()
        url = '/API/books/1'
        data = {'id': 1, 'title': 'New title', 'publishedYear': 1992, 'pages': 48, 'language': 1, 'authors': [1]}
        response = self.client.put(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get().title, 'New title')
        self.assertEqual(Book.objects.get().publishedYear, 1992)
        self.assertEqual(Book.objects.get().pages, 48)
        self.assertEqual(Book.objects.get().language, Language.objects.get())
        self.assertEqual(Book.objects.get().authors.get(), Author.objects.get())

    def test_delete_book(self):
        create_book()
        url = '/API/books/1'
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
