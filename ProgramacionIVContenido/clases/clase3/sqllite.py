import sqlite3
import os

def crear_conexion():
    """Establece una conexión con la base de datos SQLite."""
    try:
        # Verificar si el archivo de base de datos existe
        if not os.path.exists("mi_base_datos.db"):
            print("Creando nueva base de datos...")
        
        # Crear conexión (si la base de datos no existe, la crea automáticamente)
        conexion = sqlite3.connect("mi_base_datos.db")
        print("Conexión establecida exitosamente")
        return conexion
    except sqlite3.Error as error:
        print(f"Error al conectar a SQLite: {error}")
        return None

def mostrar_menu():
    """Muestra el menú principal del programa."""
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Conectar a la base de datos")
    print("2. Crear una tabla")
    print("3. Insertar datos")
    print("4. Consultar datos")
    print("5. Salir")
    return input("Seleccione una opción: ")

def crear_tabla(conexion):
    """Crea una tabla de ejemplo en la base de datos."""
    try:
        cursor = conexion.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            curso TEXT
        )
        ''')
        conexion.commit()
        print("Tabla 'estudiantes' creada con éxito")
    except sqlite3.Error as error:
        print(f"Error al crear la tabla: {error}")

def insertar_datos(conexion):
    """Inserta datos de ejemplo en la tabla estudiantes."""
    try:
        cursor = conexion.cursor()
        nombre = input("Ingrese nombre del estudiante: ")
        edad = int(input("Ingrese edad: "))
        curso = input("Ingrese curso: ")
        
        cursor.execute('''
        INSERT INTO estudiantes (nombre, edad, curso) VALUES (?, ?, ?)
        ''', (nombre, edad, curso))
        
        conexion.commit()
        print(f"Estudiante {nombre} agregado correctamente")
    except sqlite3.Error as error:
        print(f"Error al insertar datos: {error}")
    except ValueError:
        print("Error: La edad debe ser un número entero")

def consultar_datos(conexion):
    """Consulta y muestra todos los estudiantes en la base de datos."""
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM estudiantes")
        estudiantes = cursor.fetchall()
        
        if not estudiantes:
            print("No hay estudiantes registrados")
            return
            
        print("\n=== LISTA DE ESTUDIANTES ===")
        print("ID | NOMBRE | EDAD | CURSO")
        print("-" * 40)
        for estudiante in estudiantes:
            print(f"{estudiante[0]} | {estudiante[1]} | {estudiante[2]} | {estudiante[3]}")
    except sqlite3.Error as error:
        print(f"Error al consultar datos: {error}")

def main():
    """Función principal del programa."""
    conexion = None
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            conexion = crear_conexion()
        elif opcion == "2":
            if conexion:
                crear_tabla(conexion)
            else:
                print("Error: Primero debe conectarse a la base de datos")
        elif opcion == "3":
            if conexion:
                insertar_datos(conexion)
            else:
                print("Error: Primero debe conectarse a la base de datos")
        elif opcion == "4":
            if conexion:
                consultar_datos(conexion)
            else:
                print("Error: Primero debe conectarse a la base de datos")
        elif opcion == "5":
            if conexion:
                conexion.close()
                print("Conexión cerrada")
            print("Programa finalizado")
            break
        else:
            print("Opción inválida. Intente nuevamente")

if __name__ == "__main__":
    main()
