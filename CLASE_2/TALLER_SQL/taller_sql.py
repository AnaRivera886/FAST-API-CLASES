

import sqlite3

# -------------------------------------------------------------------
# 1. Conectarse y crear una tabla
# -------------------------------------------------------------------
# sqlite3.connect crea el archivo taller.db si no existe.
conexion = sqlite3.connect("taller.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER,
        promedio REAL
    )
""")
conexion.commit()
print("1. Tabla 'estudiantes' creada (o ya existia).\n")

# -------------------------------------------------------------------
# 2. Insertar datos
# -------------------------------------------------------------------
# Un solo registro con execute()
cursor.execute(
    "INSERT INTO estudiantes (nombre, edad, promedio) VALUES (?, ?, ?)",
    ("Camila", 22, 4.2)
)

# Varios registros de una vez con executemany()
datos = [
    ("Juan", 25, 3.8),
    ("Laura", 20, 4.7),
    ("Pedro", 30, 3.1),
    ("Sofia", 19, 4.5),
]
cursor.executemany(
    "INSERT INTO estudiantes (nombre, edad, promedio) VALUES (?, ?, ?)",
    datos
)

# Sin commit() los datos no quedan guardados en el archivo.
conexion.commit()
print("2. Datos insertados.\n")

# -------------------------------------------------------------------
# 3. Consultar
# -------------------------------------------------------------------
print("3. Consultas:")

cursor.execute("SELECT * FROM estudiantes")
print("   Todos:", cursor.fetchall())

cursor.execute("SELECT * FROM estudiantes WHERE edad > 20")
print("   Con filtro (edad > 20):", cursor.fetchall())

cursor.execute("SELECT * FROM estudiantes ORDER BY promedio DESC LIMIT 3")
print("   Ordenados por promedio, limite 3:", cursor.fetchall())

# fetchone() devuelve una sola fila, o None si no hay coincidencia.
cursor.execute("SELECT * FROM estudiantes WHERE id = 1")
print("   fetchone() con id=1:", cursor.fetchone())

cursor.execute("SELECT * FROM estudiantes WHERE id = 999")
print("   fetchone() con id inexistente:", cursor.fetchone())
print()

# -------------------------------------------------------------------
# 4. Actualizar y eliminar
# -------------------------------------------------------------------
cursor.execute("UPDATE estudiantes SET promedio = ? WHERE id = ?", (4.9, 1))
conexion.commit()
print("4. UPDATE -> filas afectadas:", cursor.rowcount)

cursor.execute("DELETE FROM estudiantes WHERE id = ?", (4,))
conexion.commit()
print("   DELETE -> filas afectadas:", cursor.rowcount)

# Si el id no existe, rowcount da 0 (asi se detecta un 404 mas adelante).
cursor.execute("UPDATE estudiantes SET promedio = ? WHERE id = ?", (5.0, 999))
conexion.commit()
print("   UPDATE con id inexistente -> filas afectadas:", cursor.rowcount, "\n")

# -------------------------------------------------------------------
# 5. Leer por nombre de columna
# -------------------------------------------------------------------
conexion.row_factory = sqlite3.Row  # se activa antes de la siguiente consulta
cursor = conexion.cursor()

cursor.execute("SELECT * FROM estudiantes")
fila = cursor.fetchone()
print("5. Leer por nombre de columna:")
print("   fila['nombre'] ->", fila["nombre"])
print("   dict(fila)     ->", dict(fila), "\n")

# -------------------------------------------------------------------
# Paso 4 de la guia: la trampa de la inyeccion SQL
# -------------------------------------------------------------------
print("6. Demostracion de inyeccion SQL:")

dato = "' OR '1'='1"

# INSEGURO A PROPOSITO -- nunca hacer esto en un proyecto real.
# Se concatena el dato directamente en el texto de la sentencia.
consulta_insegura = f"SELECT * FROM estudiantes WHERE nombre = '{dato}'"
cursor.execute(consulta_insegura)
print("   Consulta INSEGURA (f-string) con dato malicioso:")
print("   ->", cursor.fetchall())
print("   (deberia no encontrar a nadie, pero devuelve TODOS los registros)\n")

# SEGURO: el dato va como parametro con '?', nunca dentro del texto SQL.
cursor.execute("SELECT * FROM estudiantes WHERE nombre = ?", (dato,))
print("   Consulta SEGURA (parametrizada) con el mismo dato:")
print("   ->", cursor.fetchall())
print("   (correcto: no devuelve nada, el ataque ya no funciona)\n")

# -------------------------------------------------------------------
# Cierre de la conexion
# -------------------------------------------------------------------
conexion.close()
print("Conexion cerrada. Revisa taller.db con la extension SQLite Viewer.")