# Biblioteca personal con MariaDB y SQLAlchemy

Aplicación de línea de comandos para gestionar una biblioteca personal. Sustituye el acceso directo a SQLite
por una conexión a MariaDB utilizando SQLAlchemy como ORM.

## Requisitos
- Python 3.10+
- MariaDB 10.6+ en ejecución
- Acceso a consola para crear usuario y base de datos

## Instalación de MariaDB
### Ubuntu/Debian
```bash
sudo apt update
sudo apt install mariadb-server
```

### macOS (Homebrew)
```bash
brew install mariadb
brew services start mariadb
```

### Windows
Descarga el instalador desde [MariaDB.org](https://mariadb.org/download/) y sigue los pasos guiados.

## Configuración inicial de la base de datos
1. Inicia el servicio de MariaDB (ejemplo en Linux):
   ```bash
   sudo systemctl start mariadb
   ```
2. Crea la base de datos y el usuario dedicado:
   ```sql
   CREATE DATABASE biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'biblioteca_user'@'localhost' IDENTIFIED BY 'biblioteca_pass';
   GRANT ALL PRIVILEGES ON biblioteca.* TO 'biblioteca_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
3. (Opcional) Ejecuta `mysql_secure_installation` para endurecer la instalación.

## Configuración de la aplicación
La cadena de conexión se lee de la variable de entorno `DATABASE_URL` con el formato:
```
mariadb+pymysql://usuario:password@host:puerto/base
```
Si no se define, se usa `mariadb+pymysql://biblioteca_user:biblioteca_pass@localhost:3306/biblioteca`.

Puedes definir la variable en un archivo `.env` en la raíz del proyecto:
```
DATABASE_URL=mariadb+pymysql://biblioteca_user:biblioteca_pass@localhost:3306/biblioteca
```

## Instalación de dependencias
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Ejecución
```bash
python app.py
```
Se mostrará un menú interactivo con las opciones:
- Agregar nuevo libro
- Actualizar información de un libro
- Eliminar libro existente
- Ver listado de libros
- Buscar libros por título, autor o género
- Salir de la aplicación

## Manejo de errores
La aplicación captura y muestra mensajes cuando ocurren problemas de conexión, transacciones
fallidas o errores de integridad en la base de datos. Revisa la configuración de `DATABASE_URL`
si notas fallos de conexión.
