from django.contrib import admin
from django.urls import path, include

from google_books.urls import books_urlpatterns
from my_API.urls import api_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(books_urlpatterns)),
    path('API/', include(api_urlpatterns)),
]
