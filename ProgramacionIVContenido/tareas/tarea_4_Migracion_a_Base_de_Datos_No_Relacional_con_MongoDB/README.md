# Biblioteca personal con MongoDB

Aplicación de línea de comandos para gestionar una biblioteca personal usando MongoDB como base de datos no relacional. Todas las operaciones se realizan sobre documentos JSON almacenados en una colección.

## Requisitos previos

- Python 3.10+
- MongoDB en ejecución (local o en la nube)
- Variables de entorno configuradas para la conexión

### Instalar MongoDB localmente

#### Ubuntu/Debian (usando APT)
```bash
sudo apt update
sudo apt install -y mongodb
sudo systemctl enable --now mongodb
```

#### Docker
```bash
docker run -d \
  -p 27017:27017 \
  --name biblioteca-mongo \
  -e MONGO_INITDB_ROOT_USERNAME=biblioteca \
  -e MONGO_INITDB_ROOT_PASSWORD=seguro \
  mongo:7
```

### Usar MongoDB Atlas
1. Crea un clúster gratuito en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Genera un usuario de base de datos y habilita el acceso desde tu IP.
3. Obtén la cadena de conexión (Connection string) y guárdala para configurarla en la aplicación.

## Configuración de la conexión

Crea un archivo `.env` (puedes partir del ejemplo `.env.example`) o exporta la variable de entorno directamente:

```bash
export MONGODB_URI="mongodb://localhost:27017"
```

Para instancias protegidas agrega usuario y contraseña en la URI (por ejemplo, `mongodb://usuario:clave@localhost:27017/?authSource=admin`).

## Instalación de dependencias

```bash
pip install -r requirements.txt
```

## Ejecución de la aplicación

```bash
python biblioteca_cli.py
```

## Estructura del documento

Cada libro se almacena como un documento con la siguiente estructura mínima:

```json
{
  "titulo": "1984",
  "autor": "George Orwell",
  "genero": "Distopía",
  "estado": "pendiente",
  "creado_en": "2024-05-05T12:00:00Z"
}
```

Los valores aceptados para `estado` son `pendiente`, `leyendo` o `leido`.

## Funcionalidades

- **Agregar libro:** solicita título, autor, género y estado y crea un nuevo documento.
- **Actualizar libro:** permite modificar cualquier campo usando el ID de MongoDB.
- **Eliminar libro:** borra un documento por su ID.
- **Listar libros:** muestra todos los documentos almacenados.
- **Buscar libros:** filtra por título, autor o género con coincidencias parciales.
- **Salir:** cierra la aplicación.

## Validaciones y manejo de errores

- Verificación de conexión al iniciar la aplicación; si falla, se muestra un mensaje claro.
- Validación de campos obligatorios y valores permitidos para el estado antes de guardar o actualizar.
- Manejo de búsquedas sin resultados para informar al usuario.
- Captura de errores comunes de `pymongo` durante las operaciones CRUD.

## Ejemplos de uso

1. **Agregar libro**
   - Ingresa las opciones solicitadas. Si el estado no es válido, la aplicación lo indicará.
2. **Buscar por autor**
   - Selecciona la opción 5 y escribe parte del nombre del autor (ejemplo: `Rowling`). Se mostrarán coincidencias parciales.
3. **Actualizar estado**
   - Usa la opción 2, indica el ID del libro y un nuevo estado permitido (`leyendo`, `pendiente` o `leido`).

## Notas

- Si usas Docker para MongoDB, asegúrate de que el puerto `27017` esté accesible desde la máquina donde ejecutas la aplicación.
- Para MongoDB Atlas, verifica que la IP de tu máquina esté incluida en la lista de IPs permitidas del clúster.
