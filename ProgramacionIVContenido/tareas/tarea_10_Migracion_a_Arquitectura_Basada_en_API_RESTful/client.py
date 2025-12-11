"""Aplicación cliente Flask que consume la API RESTful de libros."""

import os
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5001")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "biblioteca-secreta")


def _api_url(path: str) -> str:
    return f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def _fetch_books() -> List[Dict]:
    try:
        response = requests.get(_api_url("books"), timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        flash("No se pudieron obtener los libros desde la API.", "error")
        return []


def _fetch_book(book_id: int) -> Optional[Dict]:
    try:
        response = requests.get(_api_url(f"books/{book_id}"), timeout=5)
        if response.status_code == 404:
            flash("No se encontró el libro solicitado.", "error")
            return None
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        flash("Error al comunicarse con la API.", "error")
        return None


def _persist_book(method: str, path: str, payload: Dict[str, str]):
    try:
        response = requests.request(method, _api_url(path), json=payload, timeout=5)
        if response.status_code in (400, 404):
            data = response.json()
            if isinstance(data, dict) and data.get("errors"):
                for error in data["errors"]:
                    flash(error, "error")
            else:
                flash(data.get("error", "La API rechazó la solicitud."), "error")
            return None
        response.raise_for_status()
        return response
    except requests.RequestException:
        flash("No fue posible contactar la API.", "error")
        return None


@app.route("/")
def index():
    books = _fetch_books()
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

        payload = {"title": title, "author": author, "year": int(year), "genre": genre}
        response = _persist_book("POST", "books", payload)
        if response:
            flash("Libro agregado correctamente.", "success")
            return redirect(url_for("index"))

    return render_template("add_book.html")


@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id: int):
    book = _fetch_book(book_id)
    if not book:
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()
        genre = request.form.get("genre", "").strip()

        if not title or not author or not year.isdigit():
            flash("Por favor completa todos los campos y verifica el año.", "error")
            return render_template("edit_book.html", book=book)

        payload = {"title": title, "author": author, "year": int(year), "genre": genre}
        response = _persist_book("PUT", f"books/{book_id}", payload)
        if response:
            flash("Libro actualizado correctamente.", "success")
            return redirect(url_for("index"))

    return render_template("edit_book.html", book=book)


@app.route("/books/<int:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id: int):
    book = _fetch_book(book_id)
    if not book:
        return redirect(url_for("index"))

    if request.method == "POST":
        response = _persist_book("DELETE", f"books/{book_id}", {})
        if response:
            flash("Libro eliminado correctamente.", "success")
            return redirect(url_for("index"))

    return render_template("confirm_delete.html", book=book)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        flash("Ingresa un término de búsqueda.", "error")
        return redirect(url_for("index"))

    books = _fetch_books()
    filtered = [
        book
        for book in books
        if query.lower() in str(book.get("title", "")).lower()
        or query.lower() in str(book.get("author", "")).lower()
        or query.lower() in str(book.get("genre", "")).lower()
    ]
    return render_template("search_results.html", query=query, results=filtered)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
