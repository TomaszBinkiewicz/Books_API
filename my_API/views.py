from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (BookSerializer,
                          Book,
                          AuthorSerializer,
                          Author,
                          LanguageSerializer,
                          Language
                          )
from google_books.views import filter_books


def home_view_api(request):
    return render(request, 'my_API/home_view.html')


class BookAPIView(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book, context={'request': request}, )
        return Response(serializer.data)

    def put(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        book = self.get_object(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllBooksAPIView(APIView):
    def get(self, request):
        books = filter_books(request)
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        book = Book.objects.create()
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        books = Book.objects.all()
        for book in books:
            book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorAPIView(APIView):
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, id):
        author = self.get_object(id)
        serializer = AuthorSerializer(author, context={'request': request}, )
        return Response(serializer.data)

    def put(self, request, id):
        author = self.get_object(id)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        author = self.get_object(id)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllAuthorsAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        author = Author.objects.create()
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        authors = Author.objects.all()
        for author in authors:
            author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LanguageAPIView(APIView):
    def get_object(self, pk):
        try:
            return Language.objects.get(pk=pk)
        except Language.DoesNotExist:
            raise Http404

    def get(self, request, id):
        language = self.get_object(id)
        serializer = LanguageSerializer(language, context={'request': request}, )
        return Response(serializer.data)

    def put(self, request, id):
        language = self.get_object(id)
        serializer = LanguageSerializer(language, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        language = self.get_object(id)
        language.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllLanguagesAPIView(APIView):
    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        language = Language.objects.create()
        serializer = LanguageSerializer(language, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        languages = Language.objects.all()
        for language in languages:
            language.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
