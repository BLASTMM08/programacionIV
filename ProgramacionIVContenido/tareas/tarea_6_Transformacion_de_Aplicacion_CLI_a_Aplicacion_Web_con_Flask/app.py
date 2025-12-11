import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from redis import Redis

from storage import BookRepository


def create_app(redis_client: Optional[Redis] = None) -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

    client = redis_client or Redis.from_url(
        os.getenv("KEYDB_URL", "redis://localhost:6379/0"), decode_responses=False
    )
    repository = BookRepository(client)

    @app.route("/")
    def index():
        query = request.args.get("q", "")
        books = repository.search(query) if query else repository.all()
        return render_template("index.html", books=books, query=query)

    @app.route("/libros/nuevo", methods=["GET", "POST"])
    def create_book():
        if request.method == "POST":
            titulo = request.form.get("titulo", "").strip()
            autor = request.form.get("autor", "").strip()
            genero = request.form.get("genero", "").strip()
            estado = request.form.get("estado", "").strip()

            if not titulo or not autor or not genero or not estado:
                flash("Todos los campos son obligatorios.", "danger")
                return render_template("form.html", book=None)

            repository.create(titulo, autor, genero, estado)
            flash("Libro agregado correctamente.", "success")
            return redirect(url_for("index"))

        return render_template("form.html", book=None)

    @app.route("/libros/<book_id>/editar", methods=["GET", "POST"])
    def edit_book(book_id: str):
        book = repository.get(book_id)
        if not book:
            flash("El libro no existe.", "warning")
            return redirect(url_for("index"))

        if request.method == "POST":
            titulo = request.form.get("titulo", "").strip()
            autor = request.form.get("autor", "").strip()
            genero = request.form.get("genero", "").strip()
            estado = request.form.get("estado", "").strip()

            if not titulo or not autor or not genero or not estado:
                flash("Todos los campos son obligatorios.", "danger")
                return render_template("form.html", book=book)

            updated = repository.update(book_id, titulo, autor, genero, estado)
            if updated:
                flash("Libro actualizado correctamente.", "success")
            else:
                flash("No se pudo actualizar el libro.", "danger")
            return redirect(url_for("index"))

        return render_template("form.html", book=book)

    @app.route("/libros/<book_id>/eliminar", methods=["POST"])
    def delete_book(book_id: str):
        if repository.delete(book_id):
            flash("Libro eliminado correctamente.", "info")
        else:
            flash("No se encontró el libro a eliminar.", "warning")
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
