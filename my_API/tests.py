from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from google_books.models import Book, Author, Language


class AllLanguagesAPITestCase(APITestCase):

    def test_create_language(self):
        url = '/API/languages'
        data = {"language": "en"}
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
