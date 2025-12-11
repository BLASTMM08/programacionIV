from itertools import count
from typing import List, Optional

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "biblioteca-secreta"


title_id_generator = count(1)


class Book:
    def __init__(self, title: str, author: str, year: int, genre: str):
        self.id = next(title_id_generator)
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre


books: List[Book] = [
    Book("El nombre del viento", "Patrick Rothfuss", 2007, "Fantasía"),
    Book("Cien años de soledad", "Gabriel García Márquez", 1967, "Realismo mágico"),
    Book("El juego de Ender", "Orson Scott Card", 1985, "Ciencia ficción"),
]


def find_book(book_id: int) -> Optional[Book]:
    return next((book for book in books if book.id == book_id), None)


@app.route("/")
def index():
    return render_template("index.html", books=books)


@app.route("/books/new", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()
        genre = request.form.get("genre", "").strip()

        if not title or not author or not year.isdigit():
            flash("Por favor completa todos los campos y verifica el año.", "error")
            return render_template("add_book.html")

        new_book = Book(title, author, int(year), genre)
        books.append(new_book)
        flash(f"Libro '{new_book.title}' agregado correctamente.", "success")
        return redirect(url_for("index"))

    return render_template("add_book.html")


@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id: int):
    book = find_book(book_id)
    if not book:
        flash("No se encontró el libro solicitado.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()
        genre = request.form.get("genre", "").strip()

        if not title or not author or not year.isdigit():
            flash("Por favor completa todos los campos y verifica el año.", "error")
            return render_template("edit_book.html", book=book)

        book.title = title
        book.author = author
        book.year = int(year)
        book.genre = genre
        flash(f"Libro '{book.title}' actualizado correctamente.", "success")
        return redirect(url_for("index"))

    return render_template("edit_book.html", book=book)


@app.route("/books/<int:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        flash("No se encontró el libro solicitado.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        books.remove(book)
        flash(f"Libro '{book.title}' eliminado.", "success")
        return redirect(url_for("index"))

    return render_template("confirm_delete.html", book=book)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        flash("Ingresa un término de búsqueda.", "error")
        return redirect(url_for("index"))

    filtered = [
        book
        for book in books
        if query.lower() in book.title.lower()
        or query.lower() in book.author.lower()
        or query.lower() in book.genre.lower()
    ]
    return render_template("search_results.html", query=query, results=filtered)


if __name__ == "__main__":
    app.run(debug=True)
