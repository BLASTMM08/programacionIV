"""Aplicación CLI para administrar una biblioteca personal con SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Optional

DB_PATH = Path(__file__).with_name("biblioteca.db")


def get_connection() -> sqlite3.Connection:
    """Crea una conexión a la base de datos y habilita el modo row factory."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """Crea la tabla de libros si no existe."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                genero TEXT NOT NULL,
                estado TEXT NOT NULL CHECK (estado IN ('Leído', 'No leído'))
            )
            """
        )


def normalizar_estado(valor: str) -> Optional[str]:
    """Normaliza el estado ingresado por el usuario."""
    texto = valor.strip().lower()
    if texto in {"leido", "leído", "l"}:
        return "Leído"
    if texto in {"no leido", "no leído", "no", "n"}:
        return "No leído"
    return None


def solicitar_estado(predeterminado: Optional[str] = None) -> str:
    """Solicita al usuario un estado de lectura válido."""
    while True:
        mensaje = "Estado de lectura [Leído/No leído]"
        if predeterminado:
            mensaje += f" ({predeterminado})"
        mensaje += ": "
        respuesta = input(mensaje)
        if not respuesta and predeterminado:
            return predeterminado
        estado = normalizar_estado(respuesta)
        if estado:
            return estado
        print("⚠️ Opción no válida. Usa 'Leído' o 'No leído'.")


def agregar_libro() -> None:
    """Solicita datos y añade un libro a la base."""
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Género: ").strip()
    estado = solicitar_estado()

    if not titulo or not autor or not genero:
        print("⚠️ Todos los campos son obligatorios. Intenta de nuevo.")
        return

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO libros (titulo, autor, genero, estado) VALUES (?, ?, ?, ?)",
            (titulo, autor, genero, estado),
        )
    print("✅ Libro agregado correctamente.\n")


def obtener_libro(id_libro: int) -> Optional[sqlite3.Row]:
    """Devuelve un registro de libro por id si existe."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM libros WHERE id = ?", (id_libro,))
        return cursor.fetchone()


def actualizar_libro() -> None:
    """Permite modificar los datos de un libro existente."""
    try:
        id_libro = int(input("ID del libro a actualizar: "))
    except ValueError:
        print("⚠️ Ingresa un número de ID válido.")
        return

    libro = obtener_libro(id_libro)
    if not libro:
        print("⚠️ No se encontró un libro con ese ID.")
        return

    print("Deja el campo vacío para mantener el valor actual.")
    titulo = input(f"Título ({libro['titulo']}): ").strip() or libro["titulo"]
    autor = input(f"Autor ({libro['autor']}): ").strip() or libro["autor"]
    genero = input(f"Género ({libro['genero']}): ").strip() or libro["genero"]
    estado = solicitar_estado(libro["estado"])

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE libros
               SET titulo = ?, autor = ?, genero = ?, estado = ?
             WHERE id = ?
            """,
            (titulo, autor, genero, estado, id_libro),
        )
    print("✅ Libro actualizado correctamente.\n")


def eliminar_libro() -> None:
    """Elimina un libro por su ID."""
    try:
        id_libro = int(input("ID del libro a eliminar: "))
    except ValueError:
        print("⚠️ Ingresa un número de ID válido.")
        return

    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
        if cursor.rowcount:
            print("✅ Libro eliminado correctamente.\n")
        else:
            print("⚠️ No se encontró un libro con ese ID.")


def imprimir_tabla(libros: Iterable[sqlite3.Row]) -> None:
    """Muestra una tabla con los libros suministrados."""
    print("\n{:<4} {:<30} {:<20} {:<15} {:<10}".format("ID", "Título", "Autor", "Género", "Estado"))
    print("-" * 85)
    for libro in libros:
        print(
            "{:<4} {:<30} {:<20} {:<15} {:<10}".format(
                libro["id"], libro["titulo"], libro["autor"], libro["genero"], libro["estado"]
            )
        )
    print()


def listar_libros() -> None:
    """Muestra todos los libros registrados."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM libros ORDER BY id")
        libros = cursor.fetchall()

    if not libros:
        print("No hay libros registrados.\n")
        return

    imprimir_tabla(libros)


def buscar_libros() -> None:
    """Permite buscar libros por título, autor o género."""
    termino = input("Ingresa término de búsqueda: ").strip()
    if not termino:
        print("⚠️ Ingresa al menos un carácter para buscar.")
        return

    comodin = f"%{termino}%"
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT * FROM libros
             WHERE titulo LIKE ? OR autor LIKE ? OR genero LIKE ?
             ORDER BY id
            """,
            (comodin, comodin, comodin),
        )
        resultados = cursor.fetchall()

    if resultados:
        imprimir_tabla(resultados)
    else:
        print("No se encontraron coincidencias.\n")


def mostrar_menu() -> None:
    """Imprime el menú principal."""
    print("""
===== Biblioteca Personal =====
1. Agregar nuevo libro
2. Actualizar información de un libro
3. Eliminar libro existente
4. Ver listado de libros
5. Buscar libros
6. Salir
""")


def ejecutar_opcion(opcion: str) -> bool:
    """Ejecuta la opción seleccionada. Devuelve False si se debe salir."""
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
        print("Hasta pronto!")
        return False
    else:
        print("⚠️ Opción no válida. Intenta nuevamente.")
    return True


def main() -> None:
    init_db()
    continuar = True
    while continuar:
        mostrar_menu()
        continuar = ejecutar_opcion(input("Selecciona una opción: ").strip())


if __name__ == "__main__":
    main()
