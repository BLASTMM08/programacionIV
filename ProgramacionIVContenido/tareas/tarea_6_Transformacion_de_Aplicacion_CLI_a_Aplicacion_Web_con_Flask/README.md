# Biblioteca personal con Flask y KeyDB

Aplicación web que permite administrar una biblioteca personal utilizando Flask como framework web y KeyDB/Redis como almacenamiento en memoria.

## Requisitos
- Python 3.11+
- Servidor KeyDB o Redis accesible

## Instalación
1. Crea un entorno virtual y activa:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Copia el archivo de entorno y ajusta valores según sea necesario:
   ```bash
   cp .env.example .env
   ```

## Ejecución
Con el entorno activado, inicia el servidor Flask:
```bash
flask --app app run --debug --host 0.0.0.0 --port 5000
```
La aplicación quedará disponible en `http://localhost:5000`.

## Funcionalidades
- Agregar, editar y eliminar libros con validaciones básicas.
- Listado general de libros almacenados en KeyDB.
- Búsqueda por título, autor o género.
- Mensajes de retroalimentación para cada operación.

