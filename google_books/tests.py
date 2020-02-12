from django.test import TestCase
from datetime import date
from django.core.exceptions import ValidationError
from google_books.utils.views_utils import (filter_books,
                                            get_author_object,
                                            get_language_object,
                                            )
from google_books.utils.models_utils import (validate_year,
                                             validate_month,
                                             validate_day,
                                             )
from .views import (get_books_from_api,
                    AllBooksView,
                    AddBookView,
                    ImportFromApiView)


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
