import os
from itertools import count
from typing import List, Optional

from celery import Celery
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mail import Mail, Message

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "biblioteca-secreta")

    app.config.update(
        MAIL_SERVER=os.getenv("MAIL_SERVER", "localhost"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", "25")),
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "False").lower() == "true",
        MAIL_USE_SSL=os.getenv("MAIL_USE_SSL", "False").lower() == "true",
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER"),
        MAIL_SUPPRESS_SEND=os.getenv("MAIL_SUPPRESS_SEND", "True").lower() == "true",
        CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")),
        NOTIFICATION_RECIPIENT=os.getenv("NOTIFICATION_RECIPIENT", os.getenv("MAIL_USERNAME")),
    )
    return app


def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = create_app()
mail = Mail(app)
celery = make_celery(app)

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


@celery.task(name="tasks.send_email")
def send_email(subject: str, recipients: List[str], body: str) -> None:
    if not recipients:
        return

    sender = app.config.get("MAIL_DEFAULT_SENDER") or app.config.get("MAIL_USERNAME")
    msg = Message(subject=subject, recipients=recipients, body=body, sender=sender)
    mail.send(msg)


def notify_change(action: str, book: Book) -> None:
    recipient = app.config.get("NOTIFICATION_RECIPIENT")
    if not recipient:
        app.logger.warning("No se definió NOTIFICATION_RECIPIENT; se omite el envío de correo.")
        return

    subject = f"Biblioteca personal: libro {action}"
    body = (
        f"Se ha {action} el libro:\n\n"
        f"Título: {book.title}\n"
        f"Autor: {book.author}\n"
        f"Año: {book.year}\n"
        f"Género: {book.genre}\n"
    )
    send_email.delay(subject, [recipient], body)


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
        notify_change("agregado", new_book)
        flash(f"Libro '{new_book.title}' agregado correctamente. Se programó el envío de correo.", "success")
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
        notify_change("eliminado", book)
        flash(f"Libro '{book.title}' eliminado. Se programó el envío de correo.", "success")
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
