# Biblioteca personal con tareas asíncronas

Aplicación Flask de la tarea 8 que gestiona una biblioteca personal y envía notificaciones por correo cuando se agregan o eliminan libros. El envío se realiza de forma asíncrona con Celery usando KeyDB/Redis como broker.

## Requisitos previos
- Python 3.10+
- KeyDB o Redis accesible (por defecto `redis://localhost:6379/0`)
- Servidor SMTP accesible o `MAIL_SUPPRESS_SEND=True` para desarrollo.

## Configuración
1. Crea un archivo `.env` a partir de `.env.example` y completa tus credenciales SMTP y la URL del broker de Celery.
2. Instala dependencias:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Ejecución
1. Inicia el worker de Celery (requiere que el broker esté disponible):
   ```bash
   celery -A app.celery worker --loglevel=info
   ```
2. En otra terminal, inicia la aplicación Flask:
   ```bash
   flask --app app run --debug
   ```

Cuando se agregue o elimine un libro desde la interfaz web, se encolará automáticamente un correo de notificación al destinatario configurado en `NOTIFICATION_RECIPIENT`.
