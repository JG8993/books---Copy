from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book 

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.fav_books= []

    @classmethod
    def get_author(cls): #retrieves all authors
        query = "SELECT * FROM authors;"
        results = connectToMySQL('books_schema_jg').query_db(query)
        authors = []
        for x in results:
            authors.append(cls(x))
        return authors

    @classmethod
    def save_author(cls, data): #saves new author
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        results = connectToMySQL('books_schema_jg').query_db(query,data)
        return results

    @classmethod #saves authors favorite book
    def save_favorite(cls,data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema_jg').query_db(query,data)
    
    @classmethod
    def not_yet_fav_author(cls,data): #retrieves unfavorited authors
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s);"
        authors = []
        results = connectToMySQL('books_schema_jg').query_db(query,data)
        for x in results:
            authors.append(cls(x))
        return authors

    @classmethod
    def get_author_by_id(cls,data): #many to many
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id= favorites.author_id LEFT JOIN books on books.id = favorites.book_id WHERE authors.id=%(id)s;"
        results = connectToMySQL('books_schema_jg').query_db(query,data)
        author= cls(results[0])
        for x in results:
            if x['books.id'] == None: 
                break #break if no favorites
            data= {
                "id": x['books.id'],
                "title": x['title'],
                "num_of_pages": x['num_of_pages'],
                "created_at": x['created_at'],
                "updated_at": x['updated_at']
            }
            author.fav_books.append(book.Book(data))
        return author