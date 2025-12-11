# Tarea 10: Migración a arquitectura basada en API RESTful

Esta entrega divide la aplicación de biblioteca en dos componentes:

- **API RESTful (`api.py`)**: expone operaciones CRUD sobre libros.
- **Cliente Flask (`client.py`)**: consume la API usando `requests` y renderiza las vistas HTML.

## Requisitos

Instala las dependencias en un entorno virtual:

```bash
pip install -r requirements.txt
```

## Variables de entorno

- `API_BASE_URL`: URL base de la API (por defecto `http://localhost:5001`).
- `FLASK_SECRET_KEY`: clave de sesión para el cliente (opcional).

Puedes crear un archivo `.env` junto a `client.py` y `api.py` para definir estas variables.

## Cómo ejecutar

1. **Iniciar la API**
   ```bash
   python api.py
   ```
   La API quedará escuchando en `http://localhost:5001`.

2. **Iniciar la aplicación cliente**
   En otra terminal y con la API en ejecución:
   ```bash
   python client.py
   ```
   Abre `http://localhost:5000` en el navegador para usar la interfaz web.

## Endpoints expuestos por la API

- `GET /books` devuelve todos los libros.
- `GET /books/<id>` devuelve un libro específico.
- `POST /books` crea un libro (requiere JSON con `title`, `author`, `year`, `genre`).
- `PUT /books/<id>` actualiza un libro existente.
- `DELETE /books/<id>` elimina un libro.

La API responde en JSON y usa códigos de estado HTTP adecuados (200, 201, 400, 404).
