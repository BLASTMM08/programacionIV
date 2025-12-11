import json
import os
from typing import List, Dict, Any

DATA_FILE = "articulos.json"


def load_articles() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_articles(articles: List[Dict[str, Any]]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)


def generate_id(articles: List[Dict[str, Any]]) -> int:
    if not articles:
        return 1
    return max(article["id"] for article in articles) + 1


def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("⚠️ El valor no puede estar vacío. Intente nuevamente.")


def input_positive_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if not value:
            print("⚠️ El valor no puede estar vacío. Intente nuevamente.")
            continue
        if not value.isdigit():
            print("⚠️ Debe ingresar un número entero positivo.")
            continue
        number = int(value)
        if number <= 0:
            print("⚠️ El número debe ser mayor a 0.")
            continue
        return number


def input_positive_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip().replace(",", ".")
        if not value:
            print("⚠️ El valor no puede estar vacío. Intente nuevamente.")
            continue
        try:
            number = float(value)
        except ValueError:
            print("⚠️ Debe ingresar un número. Ejemplo: 10.50")
            continue
        if number <= 0:
            print("⚠️ El número debe ser mayor a 0.")
            continue
        return number


def register_article(articles: List[Dict[str, Any]]) -> None:
    print("\n🆕 Registrar nuevo artículo")
    name = input_non_empty("Nombre: ")
    category = input_non_empty("Categoría: ")
    quantity = input_positive_int("Cantidad: ")
    unit_price = input_positive_float("Precio unitario: ")
    description = input_non_empty("Descripción: ")

    article = {
        "id": generate_id(articles),
        "nombre": name,
        "categoria": category,
        "cantidad": quantity,
        "precio_unitario": unit_price,
        "descripcion": description,
    }

    articles.append(article)
    save_articles(articles)
    print(f"✅ Artículo '{name}' registrado con éxito. ID asignado: {article['id']}\n")


def search_articles(articles: List[Dict[str, Any]]) -> None:
    if not articles:
        print("\nNo hay artículos registrados aún.\n")
        return

    print("\n🔍 Buscar artículos")
    criteria = input("Buscar por [n]ombre o [c]ategoría? ").strip().lower()
    if criteria not in {"n", "c"}:
        print("⚠️ Opción no válida.\n")
        return

    term = input_non_empty("Ingrese el término de búsqueda: ").lower()
    key = "nombre" if criteria == "n" else "categoria"

    results = [article for article in articles if term in article[key].lower()]

    if not results:
        print("\nNo se encontraron artículos que coincidan.\n")
        return

    print("\nResultados de búsqueda:")
    print_table(results)
    print()


def list_articles(articles: List[Dict[str, Any]]) -> None:
    if not articles:
        print("\nNo hay artículos registrados aún.\n")
        return

    print("\n📋 Lista de artículos registrados:")
    print_table(articles)
    print()


def print_table(articles: List[Dict[str, Any]]) -> None:
    headers = ["ID", "Nombre", "Categoría", "Cantidad", "Precio unitario", "Descripción"]
    rows = [
        [
            str(article["id"]),
            article["nombre"],
            article["categoria"],
            str(article["cantidad"]),
            f"${article['precio_unitario']:.2f}",
            article["descripcion"],
        ]
        for article in articles
    ]

    widths = [max(len(header), *(len(row[i]) for row in rows)) for i, header in enumerate(headers)]
    header_line = " | ".join(header.ljust(widths[i]) for i, header in enumerate(headers))
    separator = "-+-".join("-" * width for width in widths)
    print(header_line)
    print(separator)
    for row in rows:
        print(" | ".join(row[i].ljust(widths[i]) for i in range(len(headers))))


def select_article_by_id(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    list_articles(articles)
    if not articles:
        return {}

    article_id = input_positive_int("Ingrese el ID del artículo: ")
    for article in articles:
        if article["id"] == article_id:
            return article

    print("⚠️ No se encontró un artículo con ese ID.\n")
    return {}


def edit_article(articles: List[Dict[str, Any]]) -> None:
    if not articles:
        print("\nNo hay artículos para editar.\n")
        return

    print("\n✏️ Editar artículo")
    article = select_article_by_id(articles)
    if not article:
        return

    print("Deje el campo vacío para mantener el valor actual.")
    new_name = input("Nuevo nombre (actual: {}): ".format(article["nombre"])).strip()
    new_category = input("Nueva categoría (actual: {}): ".format(article["categoria"])).strip()
    new_quantity = input("Nueva cantidad (actual: {}): ".format(article["cantidad"])).strip()
    new_price = input("Nuevo precio unitario (actual: ${:.2f}): ".format(article["precio_unitario"])).strip()
    new_description = input("Nueva descripción (actual: {}): ".format(article["descripcion"])).strip()

    if new_name:
        article["nombre"] = new_name
    if new_category:
        article["categoria"] = new_category
    if new_quantity:
        if new_quantity.isdigit() and int(new_quantity) > 0:
            article["cantidad"] = int(new_quantity)
        else:
            print("⚠️ Cantidad no válida. Se mantiene el valor anterior.")
    if new_price:
        try:
            parsed_price = float(new_price.replace(",", "."))
            if parsed_price > 0:
                article["precio_unitario"] = parsed_price
            else:
                print("⚠️ El precio debe ser mayor a 0. Se mantiene el valor anterior.")
        except ValueError:
            print("⚠️ Precio no válido. Se mantiene el valor anterior.")
    if new_description:
        article["descripcion"] = new_description

    save_articles(articles)
    print("✅ Artículo actualizado con éxito.\n")


def delete_article(articles: List[Dict[str, Any]]) -> None:
    if not articles:
        print("\nNo hay artículos para eliminar.\n")
        return

    print("\n🗑️ Eliminar artículo")
    print("1) Eliminar por ID")
    print("2) Eliminar por nombre")
    option = input("Seleccione una opción: ").strip()

    if option == "1":
        article = select_article_by_id(articles)
        if not article:
            return
    elif option == "2":
        name = input_non_empty("Ingrese el nombre del artículo a eliminar: ")
        matches = [a for a in articles if a["nombre"].lower() == name.lower()]
        if not matches:
            print("⚠️ No se encontró un artículo con ese nombre.\n")
            return
        article = matches[0]
    else:
        print("⚠️ Opción no válida.\n")
        return

    articles.remove(article)
    save_articles(articles)
    print(f"✅ Artículo '{article['nombre']}' eliminado.\n")


def main_menu() -> None:
    articles = load_articles()

    print("Sistema de Registro de Presupuesto")
    print("=" * 34)

    options = {
        "1": ("Registrar un artículo", register_article),
        "2": ("Buscar artículos", search_articles),
        "3": ("Editar un artículo", edit_article),
        "4": ("Eliminar un artículo", delete_article),
        "5": ("Listar todos los artículos", list_articles),
        "0": ("Salir", None),
    }

    while True:
        print("Menú principal:")
        for key, (label, _) in options.items():
            print(f" {key}) {label}")

        choice = input("Seleccione una opción: ").strip()
        if choice == "0":
            print("👋 Hasta pronto.")
            break

        action = options.get(choice)
        if action is None:
            print("⚠️ Opción no válida. Intente nuevamente.\n")
            continue

        _, handler = action
        handler(articles)


if __name__ == "__main__":
    main_menu()
