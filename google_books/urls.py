from django.urls import path

from google_books.views import (get_books_from_api,
                                AllBooksView,
                                AddBookView,
                                ImportFromApi,
                                )

books_urlpatterns = [
    path('', get_books_from_api),
    path('books/', AllBooksView.as_view(), name='all-books'),
    path('add-book/', AddBookView.as_view(), name='add-book'),
    path('import-books/', ImportFromApi.as_view(), name='import-books'),
]
