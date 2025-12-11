# Biblioteca Personal en Consola

Aplicación de línea de comandos en Python para administrar una biblioteca personal usando SQLite.

## Requisitos previos

- Python 3.9 o superior (incluye el módulo estándar `sqlite3`).

## Instalación y ejecución

1. Clona o descarga este repositorio.
2. Abre una terminal en la carpeta `tarea_2_Desarrollo_de_Aplicacion_para_Biblioteca_Personal`.
3. Ejecuta el programa con:

```bash
python biblioteca.py
```

El archivo de base de datos `biblioteca.db` se crea automáticamente la primera vez que se ejecuta el programa.

## Funcionalidades

- **Agregar nuevo libro**: solicita título, autor, género y estado de lectura.
- **Actualizar libro**: modifica cualquier campo manteniendo el valor actual si presionas Enter.
- **Eliminar libro**: borra un registro por su ID.
- **Listar libros**: muestra todos los libros registrados en una tabla.
- **Buscar libros**: realiza coincidencias por título, autor o género.
- **Salir**: termina la ejecución del programa.

## Notas de uso

- Para el estado de lectura se aceptan variaciones como `Leído`, `leido`, `L`, `No leído`, `no`.
- El menú se muestra en bucle hasta elegir la opción **6. Salir**.
- La base de datos se almacena junto al script para facilitar su transporte.
