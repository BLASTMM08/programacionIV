from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


ALLOWED_STATUSES = {"pendiente", "leyendo", "leido"}


@dataclass
class Book:
    titulo: str
    autor: str
    genero: str
    estado: str
    creado_en: datetime = field(default_factory=datetime.utcnow)

    def to_document(self) -> Dict[str, object]:
        return {
            "titulo": self.titulo.strip(),
            "autor": self.autor.strip(),
            "genero": self.genero.strip(),
            "estado": self.estado.strip().lower(),
            "creado_en": self.creado_en,
        }


class LibraryManager:
    def __init__(self, uri: str, db_name: str = "biblioteca", collection_name: str = "libros"):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]
        self._check_connection()

    def _check_connection(self) -> None:
        self.client.admin.command("ping")

    def add_book(self, book: Book) -> ObjectId:
        self._validate_book(book)
        result = self.collection.insert_one(book.to_document())
        return result.inserted_id

    def update_book(self, book_id: str, updates: Dict[str, str]) -> bool:
        filtered_updates = self._validate_updates(updates)
        if not filtered_updates:
            raise ValueError("No hay datos válidos para actualizar.")

        result = self.collection.update_one({"_id": ObjectId(book_id)}, {"$set": filtered_updates})
        return result.modified_count > 0

    def delete_book(self, book_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0

    def list_books(self) -> List[Dict[str, object]]:
        return list(self.collection.find())

    def search_books(
        self, titulo: Optional[str] = None, autor: Optional[str] = None, genero: Optional[str] = None
    ) -> List[Dict[str, object]]:
        filters: Dict[str, object] = {}
        if titulo:
            filters["titulo"] = {"$regex": titulo, "$options": "i"}
        if autor:
            filters["autor"] = {"$regex": autor, "$options": "i"}
        if genero:
            filters["genero"] = {"$regex": genero, "$options": "i"}

        return list(self.collection.find(filters))

    def _validate_book(self, book: Book) -> None:
        if not book.titulo.strip():
            raise ValueError("El título es obligatorio.")
        if not book.autor.strip():
            raise ValueError("El autor es obligatorio.")
        if not book.genero.strip():
            raise ValueError("El género es obligatorio.")
        if book.estado.strip().lower() not in ALLOWED_STATUSES:
            raise ValueError(f"Estado inválido. Valores permitidos: {', '.join(sorted(ALLOWED_STATUSES))}.")

    def _validate_updates(self, updates: Dict[str, str]) -> Dict[str, str]:
        valid_updates: Dict[str, str] = {}
        for key in ("titulo", "autor", "genero"):
            if updates.get(key):
                value = updates[key].strip()
                if not value:
                    raise ValueError(f"{key.title()} no puede estar vacío.")
                valid_updates[key] = value

        if "estado" in updates:
            estado = updates["estado"].strip().lower()
            if estado not in ALLOWED_STATUSES:
                raise ValueError(f"Estado inválido. Valores permitidos: {', '.join(sorted(ALLOWED_STATUSES))}.")
            valid_updates["estado"] = estado

        return valid_updates


def _prompt_input(prompt: str) -> str:
    return input(prompt).strip()


def _print_book(book: Dict[str, object]) -> None:
    print(f"ID: {book.get('_id')}")
    print(f"  Título: {book.get('titulo')}")
    print(f"  Autor: {book.get('autor')}")
    print(f"  Género: {book.get('genero')}")
    print(f"  Estado: {book.get('estado')}")
    creado = book.get("creado_en")
    if isinstance(creado, datetime):
        print(f"  Creado en: {creado.isoformat()}")
    print("-")


def _handle_errors(action: str, func) -> None:
    try:
        func()
    except (PyMongoError, ValueError) as exc:
        print(f"Error al {action}: {exc}")


def main() -> None:
    load_dotenv()
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    print("Conectando a MongoDB...")
    manager = None
    try:
        manager = LibraryManager(uri)
    except PyMongoError as exc:
        print(f"No se pudo conectar a MongoDB: {exc}")
        return

    menu = """
--- Biblioteca Personal con MongoDB ---
1. Agregar libro
2. Actualizar libro
3. Eliminar libro
4. Listar libros
5. Buscar libros
6. Salir
Elige una opción: """

    while True:
        opcion = _prompt_input(menu)

        if opcion == "1":
            def add_flow() -> None:
                titulo = _prompt_input("Título: ")
                autor = _prompt_input("Autor: ")
                genero = _prompt_input("Género: ")
                estado = _prompt_input("Estado (pendiente|leyendo|leido): ")
                book = Book(titulo=titulo, autor=autor, genero=genero, estado=estado)
                book_id = manager.add_book(book)
                print(f"Libro agregado con ID: {book_id}")

            _handle_errors("agregar", add_flow)

        elif opcion == "2":
            def update_flow() -> None:
                book_id = _prompt_input("ID del libro a actualizar: ")
                updates = {
                    "titulo": _prompt_input("Nuevo título (o enter para omitir): "),
                    "autor": _prompt_input("Nuevo autor (o enter para omitir): "),
                    "genero": _prompt_input("Nuevo género (o enter para omitir): "),
                    "estado": _prompt_input("Nuevo estado (pendiente|leyendo|leido, enter para omitir): "),
                }
                success = manager.update_book(book_id, updates)
                if success:
                    print("Libro actualizado correctamente.")
                else:
                    print("No se encontró el libro o no hubo cambios.")

            _handle_errors("actualizar", update_flow)

        elif opcion == "3":
            def delete_flow() -> None:
                book_id = _prompt_input("ID del libro a eliminar: ")
                success = manager.delete_book(book_id)
                if success:
                    print("Libro eliminado correctamente.")
                else:
                    print("No se encontró el libro para eliminar.")

            _handle_errors("eliminar", delete_flow)

        elif opcion == "4":
            def list_flow() -> None:
                libros = manager.list_books()
                if not libros:
                    print("No hay libros registrados.")
                    return
                for libro in libros:
                    _print_book(libro)

            _handle_errors("listar", list_flow)

        elif opcion == "5":
            def search_flow() -> None:
                titulo = _prompt_input("Buscar por título (enter para omitir): ")
                autor = _prompt_input("Buscar por autor (enter para omitir): ")
                genero = _prompt_input("Buscar por género (enter para omitir): ")
                resultados = manager.search_books(titulo=titulo or None, autor=autor or None, genero=genero or None)
                if not resultados:
                    print("No se encontraron libros con esos criterios.")
                    return
                for libro in resultados:
                    _print_book(libro)

            _handle_errors("buscar", search_flow)

        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
