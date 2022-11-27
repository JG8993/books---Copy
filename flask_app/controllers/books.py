from flask_app import app
from flask import session, redirect, render_template, request
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route('/books')
def books():
    books = Book.get_book()
    return render_template("books.html", return_books = books)

@app.route('/create_book', methods=['POST'])
def create_book():
    data= {
        'title': request.form['title'],
        'num_of_pages': request.form['num_of_pages']
    }
    Book.save_book(data)
    return redirect('/books')

@app.route('/book/<int:id>')
def display_book(id):
    data = {
        "id": id
    }
    return render_template('show_books.html', book= Book.get_book_by_id(data), unfav_authors= Author.not_yet_fav_author(data))

@app.route('/join_author', methods=['POST'])
def join_author():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.save_favorite(data)
    return redirect(f"/book/{request.form['book_id']}")