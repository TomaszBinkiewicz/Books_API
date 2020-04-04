# Content
* [Description](#books_api)
* [REST API endpoints](#endpoints)
    * [/API/books](#apibookshttpbooks-api-newherokuappcomapibooks)
    * [/API/books/{id}](#apibooksidhttpbooks-api-newherokuappcomapibooks127)
    * [/API/authors](#apiauthorshttpbooks-api-newherokuappcomapiauthors)
    * [/API/authors/{id}](#apiauthorsidhttpbooks-api-newherokuappcomapiauthors1)
    * [/API/languages](#apilanguageshttpbooks-api-newherokuappcomapilanguages)
    * [/API/languages/{id}](#apilanguagesidhttpbooks-api-newherokuappcomapilanguages1)

# Books_API
Django application which allows/contains:
* Acquiring data from public google books API
* Importing data from API (using keywords)
* Filtering and displaying records information
* Adding new records
* REST API

You can checkout this app [here](http://books-api-new.herokuapp.com)

## Endpoints

### [`/API/books`](http://books-api-new.herokuapp.com/API/books)
* `GET` - returns all books from database

    When sending HTTP GET request on /API/books you can perform filtering on books collection by passing several optional parameters:
    * title - returns results where the text following this keyword is found in the title
    * author - returns results where the text following this keyword is found in the author
    * year_from - returns results where year of publication is greater than or equal to number following this keyword
    * year_to - returns results where year of publication is lower than or equal to number following this keyword
    * language - returns results where the text following this keyword is found in language

    *request example (with some optional parameters)*
    ```
    curl --location --request GET 'http://books-api-new.herokuapp.com/API/books?author=Tolkien&title=Hobbit&language=en'
    ```

* `POST` - add new book to database

    *request example*
    ```
    curl --location --request POST 'http://books-api-new.herokuapp.com/API/books' \
    --header 'Content-Type: application/json' \
    --data-raw '{"title":"Python Web Development with Django","publishedYear":2008,"publishedMonth":10,"publishedDay":24,"isbn_10":"0132701812","isbn_13":"9780132701815","pages":408,"cover":"http://books.google.com/books/content?id=M2D5nnYlmZoC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api","language":1,"authors":[42,107,108]}'
    ```

* `DELETE` - delete whole collection of books from database

    *request example*
    ```
    curl --location --request DELETE 'http://books-api-new.herokuapp.com/API/books'
    ```

### [`/API/books/{id}`](http://books-api-new.herokuapp.com/API/books/127)
* `GET` - returns book with given id

    *request example*
    ```
    curl --location --request GET 'http://books-api-new.herokuapp.com/API/books/127'
    ```

* `PUT` - edits book with given id

    *request example*
    ```
    curl --location --request PUT 'http://books-api-new.herokuapp.com/API/books/127' \
    --header 'Content-Type: application/json' \
    --data-raw '{"id":127,"title":"Amazing Python Web Development with Django","publishedYear":2012,"publishedMonth":9,"publishedDay":27,"isbn_10":"0132701812","isbn_13":"9780132701815","pages":408,"cover":"http://books.google.com/books/content?id=M2D5nnYlmZoC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api","language":2,"authors":[42,107,108]}'
    ```

* `DELETE` - delete book with given id

    *request example*
    ```
    curl --location --request DELETE 'http://books-api-new.herokuapp.com/API/books/127'
    ```

### [`/API/authors`](http://books-api-new.herokuapp.com/API/authors)
* `GET` - returns all authors from database

    *request example*
    ```
    curl --location --request GET 'http://books-api-new.herokuapp.com/API/authors'
    ```

* `POST` - add new author to database

    *request example*
    ```
    curl --location --request POST 'http://127.0.0.1:8000/API/authors' \
    --header 'Content-Type: application/json' \
    --data-raw '{"name":"J.R.R. Tolkien"}'
    ```

* `DELETE` - delete whole collection of authors from database

    *request example*
    ```
    curl --location --request DELETE 'http://books-api-new.herokuapp.com/API/authors'
    ```

### [`/API/authors/{id}`](http://books-api-new.herokuapp.com/API/authors/1)
* `GET` - returns author with given id

    *request example*
    ```
    curl --location --request GET 'http://books-api-new.herokuapp.com/API/authors/1'
    ```

* `PUT` - edits author with given id

    *request example*
    ```
    curl --location --request PUT 'http://127.0.0.1:8000/API/authors/1' \
    --header 'Content-Type: application/json' \
    --data-raw '{"name":"John Ronald Reuel Tolkien"}'
    ```

* `DELETE` - delete author with given id

    *request example*
    ```
    curl --location --request DELETE 'http://books-api-new.herokuapp.com/API/authors/1'
    ```

### [`/API/languages`](http://books-api-new.herokuapp.com/API/languages)
* `GET` - returns all languages from database

    *request example*
    ```
    curl --location --request GET 'http://books-api-new.herokuapp.com/API/languages'
    ```

* `POST` - add new language to database

    *request example*
    ```
    curl --location --request POST 'http://books-api-new.herokuapp.com/API/languages' \
    --header 'Content-Type: application/json' \
    --data-raw '{"language":"en"}'
    ```

* `DELETE` - delete whole collection of languages from database

    *request example*
    ```
    curl --location --request DELETE 'http://books-api-new.herokuapp.com/API/languages'
    ```

### [`/API/languages/{id}`](http://books-api-new.herokuapp.com/API/languages/1)
* `GET` - returns language with given id

    *request example*
    ```
    curl --location --request GET 'http://books-api-new.herokuapp.com/API/languages/1'
    ```

* `PUT` - edits language with given id

    *request example*
    ```
    curl --location --request PUT 'http://books-api-new.herokuapp.com/API/languages/1' \
    --header 'Content-Type: application/json' \
    --data-raw '{"language":"pl"}'
    ```

* `DELETE` - delete language with given id

    *request example*
    ```
    curl --location --request DELETE 'http://books-api-new.herokuapp.com/API/languages/1'
    ```
