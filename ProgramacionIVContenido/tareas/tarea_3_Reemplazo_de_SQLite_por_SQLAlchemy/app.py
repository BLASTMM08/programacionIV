"""Aplicación de línea de comandos para gestionar una biblioteca personal usando MariaDB + SQLAlchemy."""
from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select

from database import DatabaseError, get_session, init_db
from models import Book

MENU = """
==============================
 Biblioteca personal
==============================
1. Agregar nuevo libro
2. Actualizar información de un libro
3. Eliminar libro
4. Ver listado de libros
5. Buscar libros
6. Salir
Seleccione una opción: """


def mostrar_libros(libros: Iterable[Book]) -> None:
    print("\n--- Libros registrados ---")
    for libro in libros:
        print(
            f"ID: {libro.id} | Título: {libro.title} | Autor: {libro.author} | "
            f"Género: {libro.genre} | Estado: {libro.status}"
        )
    print("-------------------------\n")


def agregar_libro() -> None:
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Género: ").strip()
    estado = input("Estado de lectura (pendiente/en progreso/completado): ").strip()

    nuevo = Book(title=titulo, author=autor, genre=genero, status=estado)
    try:
        for session in get_session():
            session.add(nuevo)
        print("Libro agregado correctamente.\n")
    except DatabaseError as exc:
        print(f"No se pudo agregar el libro: {exc}\n")


def seleccionar_libro() -> Optional[Book]:
    try:
        book_id = int(input("Ingrese el ID del libro: "))
    except ValueError:
        print("El ID debe ser un número entero.\n")
        return None

    try:
        for session in get_session():
            libro = session.get(Book, book_id)
            if not libro:
                print("No se encontró un libro con ese ID.\n")
                return None
            return libro
    except DatabaseError as exc:
        print(f"Error al buscar el libro: {exc}\n")
        return None


def actualizar_libro() -> None:
    libro = seleccionar_libro()
    if not libro:
        return

    print("Deje el campo vacío para conservar el valor actual.")
    nuevo_titulo = input(f"Título ({libro.title}): ").strip() or libro.title
    nuevo_autor = input(f"Autor ({libro.author}): ").strip() or libro.author
    nuevo_genero = input(f"Género ({libro.genre}): ").strip() or libro.genre
    nuevo_estado = input(f"Estado ({libro.status}): ").strip() or libro.status

    try:
        for session in get_session():
            libro_db = session.get(Book, libro.id)
            if libro_db:
                libro_db.title = nuevo_titulo
                libro_db.author = nuevo_autor
                libro_db.genre = nuevo_genero
                libro_db.status = nuevo_estado
        print("Libro actualizado correctamente.\n")
    except DatabaseError as exc:
        print(f"No se pudo actualizar el libro: {exc}\n")


def eliminar_libro() -> None:
    libro = seleccionar_libro()
    if not libro:
        return

    try:
        for session in get_session():
            libro_db = session.get(Book, libro.id)
            if libro_db:
                session.delete(libro_db)
                print("Libro eliminado correctamente.\n")
    except DatabaseError as exc:
        print(f"No se pudo eliminar el libro: {exc}\n")


def listar_libros() -> None:
    try:
        for session in get_session():
            libros = session.execute(select(Book)).scalars().all()
            if not libros:
                print("No hay libros registrados.\n")
                return
            mostrar_libros(libros)
    except DatabaseError as exc:
        print(f"No se pudieron listar los libros: {exc}\n")


def buscar_libros() -> None:
    criterio = input("Buscar por (titulo/autor/genero): ").strip().lower()
    valor = input("Valor a buscar: ").strip()

    campo = {
        "titulo": Book.title,
        "autor": Book.author,
        "genero": Book.genre,
    }.get(criterio)

    if campo is None:
        print("Criterio inválido. Use titulo, autor o genero.\n")
        return

    try:
        for session in get_session():
            resultados = session.execute(select(Book).where(campo.ilike(f"%{valor}%"))).scalars().all()
            if resultados:
                mostrar_libros(resultados)
            else:
                print("No se encontraron coincidencias.\n")
    except DatabaseError as exc:
        print(f"No se pudieron buscar los libros: {exc}\n")


def main() -> None:
    init_db()
    while True:
        try:
            opcion = input(MENU)
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            actualizar_libro()
        elif opcion == "3":
            eliminar_libro()
        elif opcion == "4":
            listar_libros()
        elif opcion == "5":
            buscar_libros()
        elif opcion == "6":
            print("Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.\n")


if __name__ == "__main__":
    main()
