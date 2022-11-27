from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_favorite = []

    @classmethod
    def get_book(cls):
        query =  "SELECT * FROM books;"
        results =connectToMySQL('books_schema_jg').query_db(query)
        books =[]
        for x in results:
            books.append(cls(x))
        return books

    @classmethod
    def save_book(cls,data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        return connectToMySQL("books_schema_jg").query_db(query,data)

    
    @classmethod
    def not_yet_fav_book(cls,data): 
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s);"
        books = []
        results = connectToMySQL('books_schema_jg').query_db(query,data)
        for x in results:
            books.append(cls(x))
        return books

    @classmethod
    def get_book_by_id(cls,data): #many to many
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id= favorites.book_id LEFT JOIN authors on authors.id = favorites.author_id WHERE books.id=%(id)s;"
        results = connectToMySQL('books_schema_jg').query_db(query,data)
        books = cls(results[0])
        for x in results:
            if x['authors.id'] == None: 
                break #break if no favorites
            data= {
                "id": x['authors.id'],
                "name": x['name'],
                "created_at": x['created_at'],
                "updated_at": x['updated_at']
            }
            books.authors_favorite.append(author.Author(data))
        return books
