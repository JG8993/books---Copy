from flask_app import app
from flask import redirect, request, session, render_template
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route('/')
def index():
    return redirect ('/authors')

@app.route('/authors')
def authors():
    authors = Author.get_author()
    return render_template("authors.html", return_authors = authors)

@app.route('/create_author',methods=["POST"])
def create_author():
    data = {
        "name": request.form['name']
    }
    Author.save_author(data)
    return redirect('/authors')

@app.route('/author/<int:id>')
def display_author(id):
    data = {
        "id": id
    }
    return render_template('show_authors.html', author= Author.get_author_by_id(data), unfav_books= Book.not_yet_fav_book(data))

@app.route('/join_book', methods=['POST'])
def join_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.save_favorite(data)
    return redirect(f"/author/{request.form['author_id']}")