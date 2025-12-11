# Migración a KeyDB como almacenamiento en memoria

Esta tarea adapta la aplicación de biblioteca personal para usar KeyDB (compatible con Redis) como sistema de almacenamiento en memoria. Cada libro se guarda como un objeto JSON bajo la clave `book:<id>`.

## Requisitos

- Python 3.10+
- Un servidor KeyDB o Redis accesible.
- Variables de entorno definidas en un archivo `.env` (puedes guiarte por `.env.example`).

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Configuración de entorno

Copia el archivo de ejemplo y ajusta los valores según tu entorno:

```bash
cp .env.example .env
```

Variables disponibles:

- `KEYDB_HOST`: host del servidor (por defecto `localhost`).
- `KEYDB_PORT`: puerto del servidor (por defecto `6379`).
- `KEYDB_PASSWORD`: contraseña si aplica.
- `KEYDB_DB`: base de datos numérica a usar (por defecto `0`).

## Uso de la aplicación CLI

Ejecuta el gestor interactivo con:

```bash
python app.py
```

El menú permite:

1. Agregar nuevos libros.
2. Actualizar información de un libro existente.
3. Eliminar un libro.
4. Ver el listado completo de libros.
5. Buscar libros por título, autor o género.
6. Salir del programa.

Los libros se almacenan serializados en KeyDB y se identifican con un ID incremental generado por la clave `book:id`.
