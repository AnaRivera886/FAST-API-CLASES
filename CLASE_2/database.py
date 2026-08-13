import sqlite3

# Nombre del archivo de la base de datos
DB_NAME = "tienda.db"



# Obtener una conexión a la base de datos

def obtener_conexion():
    conexion = sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )

    # Permite acceder a las columnas por nombre
    conexion.row_factory = sqlite3.Row

    # Activa las llaves foráneas en SQLite
    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion



# Crear las tablas

def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Tabla de categorías
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT
        )
    """)

    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria_id INTEGER NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()



# Insertar datos iniciales

def sembrar_datos():
    import bcrypt

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Comprobar si ya existen categorías
    cursor.execute("SELECT COUNT(*) FROM categorias")
    cantidad_categorias = cursor.fetchone()[0]

    if cantidad_categorias == 0:
        cursor.executemany("""
            INSERT INTO categorias (nombre, descripcion)
            VALUES (?, ?)
        """, [
            ("Perifericos", "Teclados, mouse y accesorios"),
            ("Pantallas", "Monitores y pantallas"),
            ("Audio", "Audifonos y dispositivos de audio")
        ])

    # Comprobar si ya existen productos
    cursor.execute("SELECT COUNT(*) FROM productos")
    cantidad_productos = cursor.fetchone()[0]

    if cantidad_productos == 0:
        cursor.executemany("""
            INSERT INTO productos (nombre, precio, categoria_id)
            VALUES (?, ?, ?)
        """, [
            ("Teclado mecanico", 120000, 1),
            ("Mouse gamer", 85000, 1),
            ("Monitor 24", 650000, 2)
        ])

    # Comprobar si ya existen usuarios
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    cantidad_usuarios = cursor.fetchone()[0]

    if cantidad_usuarios == 0:

        password_admin = bcrypt.hashpw(
            "admin123".encode(),
            bcrypt.gensalt()
        ).decode()

        password_ana = bcrypt.hashpw(
            "ana123".encode(),
            bcrypt.gensalt()
        ).decode()

        cursor.executemany("""
            INSERT INTO usuarios (username, nombre, password, rol)
            VALUES (?, ?, ?, ?)
        """, [
            ("admin", "Administrador", password_admin, "admin"),
            ("ana", "Ana Cliente", password_ana, "cliente")
        ])

    conexion.commit()
    conexion.close()