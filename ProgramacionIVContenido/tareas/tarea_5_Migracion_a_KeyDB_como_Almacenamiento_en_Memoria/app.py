import sys
from typing import Optional

from book import Book
from config import keydb_settings
from keydb_library import BookNotFoundError, KeyDBLibrary


def prompt(text: str) -> str:
    return input(text).strip()


def prompt_optional(text: str) -> Optional[str]:
    value = input(text).strip()
    return value or None


def create_library() -> KeyDBLibrary:
    settings = keydb_settings()
    return KeyDBLibrary(
        host=settings["host"],
        port=settings["port"],
        password=settings.get("password"),
        db=settings["db"],
    )


def add_book_flow(library: KeyDBLibrary) -> None:
    print("\n--- Agregar nuevo libro ---")
    title = prompt("Título: ")
    author = prompt("Autor: ")
    genre = prompt("Género: ")
    status = prompt("Estado de lectura: ")
    book = Book(title=title, author=author, genre=genre, status=status)
    created = library.add_book(book)
    print(f"Libro agregado con ID {created.id}\n")


def list_books_flow(library: KeyDBLibrary) -> None:
    print("\n--- Listado de libros ---")
    books = library.list_books()
    if not books:
        print("No hay libros registrados.\n")
        return
    for book in books:
        print(format_book(book))
    print()


def update_book_flow(library: KeyDBLibrary) -> None:
    print("\n--- Actualizar libro ---")
    try:
        book_id = int(prompt("Ingrese el ID del libro a actualizar: "))
    except ValueError:
        print("ID inválido.\n")
        return

    try:
        book = library.get_book(book_id)
    except BookNotFoundError as exc:
        print(f"{exc}\n")
        return

    print("Deje el campo vacío para conservar el valor actual.")
    new_title = prompt_optional(f"Título ({book.title}): ")
    new_author = prompt_optional(f"Autor ({book.author}): ")
    new_genre = prompt_optional(f"Género ({book.genre}): ")
    new_status = prompt_optional(f"Estado ({book.status}): ")

    updated = library.update_book(
        book_id,
        title=new_title or book.title,
        author=new_author or book.author,
        genre=new_genre or book.genre,
        status=new_status or book.status,
    )
    print("Libro actualizado:")
    print(format_book(updated))
    print()


def delete_book_flow(library: KeyDBLibrary) -> None:
    print("\n--- Eliminar libro ---")
    try:
        book_id = int(prompt("Ingrese el ID del libro a eliminar: "))
    except ValueError:
        print("ID inválido.\n")
        return

    try:
        library.delete_book(book_id)
        print("Libro eliminado correctamente.\n")
    except BookNotFoundError as exc:
        print(f"{exc}\n")


def search_books_flow(library: KeyDBLibrary) -> None:
    print("\n--- Buscar libros ---")
    title = prompt_optional("Buscar por título: ")
    author = prompt_optional("Buscar por autor: ")
    genre = prompt_optional("Buscar por género: ")
    results = library.search_books(title=title, author=author, genre=genre)
    if not results:
        print("No se encontraron coincidencias.\n")
        return
    print("Resultados:")
    for book in results:
        print(format_book(book))
    print()


def format_book(book: Book) -> str:
    return (
        f"ID: {book.id}\n"
        f"  Título: {book.title}\n"
        f"  Autor: {book.author}\n"
        f"  Género: {book.genre}\n"
        f"  Estado: {book.status}\n"
    )


def main() -> None:
    library = create_library()
    try:
        library.ping()
    except Exception as exc:  # noqa: BLE001 - mostrar mensaje amigable
        print(f"No fue posible conectar con KeyDB: {exc}")
        sys.exit(1)

    actions = {
        "1": add_book_flow,
        "2": update_book_flow,
        "3": delete_book_flow,
        "4": list_books_flow,
        "5": search_books_flow,
        "6": lambda _: sys.exit(0),
    }

    while True:
        print(
            """
Gestor de Biblioteca (KeyDB)
1. Agregar nuevo libro
2. Actualizar información de un libro
3. Eliminar libro existente
4. Ver listado de libros
5. Buscar libros
6. Salir
"""
        )
        choice = input("Seleccione una opción: ").strip()
        action = actions.get(choice)
        if action:
            try:
                action(library)
            except Exception as exc:  # noqa: BLE001 - retroalimentación general
                print(f"Ocurrió un error: {exc}\n")
        else:
            print("Opción inválida, intente de nuevo.\n")


if __name__ == "__main__":
    main()
