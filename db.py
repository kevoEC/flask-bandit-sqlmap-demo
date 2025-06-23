import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT
        )
    ''')
    cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES ('Alice', 'alice@ejemplo.com')")
    cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES ('Bob', 'bob@ejemplo.com')")
    conn.commit()
    conn.close()

crear_base_datos()
