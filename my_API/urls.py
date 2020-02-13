from django.urls import path
from my_API.views import (home_view_api,
                          BookAPIView,
                          AllBooksAPIView,
                          AuthorAPIView,
                          AllAuthorsAPIView,
                          LanguageAPIView,
                          AllLanguagesAPIView,
                          )

api_urlpatterns = [
    path('', home_view_api, name='home-view'),
    path('books', AllBooksAPIView.as_view(), name='books-list'),
    path('books/<int:id>', BookAPIView.as_view(), name='books-details'),
    path('authors', AllAuthorsAPIView.as_view(), name='authors-list'),
    path('authors/<int:id>', AuthorAPIView.as_view(), name='authors-details'),
    path('languages', AllLanguagesAPIView.as_view(), name='languages-list'),
    path('languages/<int:id>', LanguageAPIView.as_view(), name='languages-details'),
]
