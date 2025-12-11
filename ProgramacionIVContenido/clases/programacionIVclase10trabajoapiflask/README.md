# API de restaurante con Flask

Aplicación de ejemplo para la clase 10. Expone un API REST minimalista para gestionar los platillos de un restaurante usando Flask.

## Requisitos

- Python 3.10+
- Dependencias del archivo [`requirements.txt`](requirements.txt)

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar

Desde la carpeta `programacionIVclase10trabajoapiflask` ejecuta:

```bash
export FLASK_APP=app.py
flask run --debug
```

El servidor se levanta en `http://127.0.0.1:5000/` y expone los siguientes endpoints:

- `GET /platillos`: Lista todos los platillos disponibles.
- `GET /platillos/<id>`: Devuelve el detalle de un platillo.
- `POST /platillos`: Crea un nuevo platillo (requiere JSON con `nombre` y `precio`).
- `PUT /platillos/<id>`: Actualiza un platillo existente.
- `DELETE /platillos/<id>`: Elimina un platillo.

El cuerpo base para crear o actualizar platillos es:

```json
{
  "nombre": "Nombre del platillo",
  "precio": 9.99,
  "descripcion": "Descripción opcional",
  "disponible": true
}
```

## Notas

La información se guarda en memoria para fines demostrativos. Reiniciar la aplicación restablece los datos de ejemplo.
