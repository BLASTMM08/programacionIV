"""API RESTful para gestión de libros.

Este servicio expone operaciones CRUD para que una aplicación cliente
consuma los datos a través de HTTP. Utiliza almacenamiento en memoria
con datos de ejemplo para simplificar las pruebas locales.
"""

from itertools import count
from typing import Dict, List, Optional

from flask import Flask, jsonify, request

app = Flask(__name__)

_id_generator = count(1)


Book = Dict[str, object]


def _next_id() -> int:
    return next(_id_generator)


def _build_book(title: str, author: str, year: int, genre: str) -> Book:
    return {
        "id": _next_id(),
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
    }


books: List[Book] = [
    _build_book("El nombre del viento", "Patrick Rothfuss", 2007, "Fantasía"),
    _build_book("Cien años de soledad", "Gabriel García Márquez", 1967, "Realismo mágico"),
    _build_book("El juego de Ender", "Orson Scott Card", 1985, "Ciencia ficción"),
]


def _find_book(book_id: int) -> Optional[Book]:
    return next((book for book in books if book["id"] == book_id), None)


def _parse_year(raw_year: object) -> Optional[int]:
    try:
        return int(raw_year)
    except (TypeError, ValueError):
        return None


def _validate_payload(data: Dict[str, object]) -> Dict[str, object]:
    errors = []

    title = str(data.get("title", "")).strip()
    author = str(data.get("author", "")).strip()
    year = _parse_year(data.get("year"))
    genre = str(data.get("genre", "")).strip()

    if not title:
        errors.append("El título es obligatorio.")
    if not author:
        errors.append("El autor es obligatorio.")
    if year is None:
        errors.append("El año debe ser un número entero.")

    if errors:
        return {"errors": errors}

    return {"title": title, "author": author, "year": year, "genre": genre}


@app.route("/books", methods=["GET"])
def list_books():
    return jsonify(books), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def retrieve_book(book_id: int):
    book = _find_book(book_id)
    if not book:
        return jsonify({"error": "Libro no encontrado"}), 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json(silent=True) or {}
    validated = _validate_payload(data)

    if "errors" in validated:
        return jsonify(validated), 400

    new_book = _build_book(
        validated["title"], validated["author"], int(validated["year"]), validated["genre"]
    )
    books.append(new_book)
    response = jsonify(new_book)
    response.status_code = 201
    response.headers["Location"] = f"/books/{new_book['id']}"
    return response


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id: int):
    book = _find_book(book_id)
    if not book:
        return jsonify({"error": "Libro no encontrado"}), 404

    data = request.get_json(silent=True) or {}
    validated = _validate_payload(data)

    if "errors" in validated:
        return jsonify(validated), 400

    book.update(
        {
            "title": validated["title"],
            "author": validated["author"],
            "year": int(validated["year"]),
            "genre": validated["genre"],
        }
    )
    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id: int):
    book = _find_book(book_id)
    if not book:
        return jsonify({"error": "Libro no encontrado"}), 404

    books.remove(book)
    return jsonify({"message": "Libro eliminado correctamente"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
