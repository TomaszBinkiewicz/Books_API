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
    path('', home_view_api),
    path('books', AllBooksAPIView.as_view()),
    path('books/<int:id>', BookAPIView.as_view()),
    path('authors', AllAuthorsAPIView.as_view()),
    path('authors/<int:id>', AuthorAPIView.as_view()),
    path('languages', AllLanguagesAPIView.as_view()),
    path('languages/<int:id>', LanguageAPIView.as_view()),
]
