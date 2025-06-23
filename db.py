import sqlite3

def crear_tabla_usuarios():
    conn = sqlite3.connect("datos.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            clave TEXT NOT NULL,
            correo TEXT
        )
    ''')
    conn.commit()
    conn.close()

