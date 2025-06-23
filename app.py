from flask import Flask, render_template, request, redirect, jsonify, session, url_for
import os
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_super_secreta"  # Requerida para usar sesiones

# 🟩 Base de datos: asegurar que exista la tabla usuarios
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

crear_tabla_usuarios()

# 🟩 LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["username"]
        password = request.form["password"]

        # 🔥 Log intencional y ejecución shell (vulnerabilidad)
        with open("log.txt", "a") as f:
            f.write(f"{usuario}:{password}\n")
        os.system("echo " + usuario)

        # Validación sin hash
        conn = sqlite3.connect("datos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre = ? AND clave = ?", (usuario, password))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            session["usuario"] = usuario
            return redirect("/bienvenido")
        else:
            return "<h3>Acceso denegado</h3>"

    return render_template("login.html")

# 🟥 SQL Injection
@app.route("/buscar")
def buscar_usuario():
    id_usuario = request.args.get("id")
    conn = sqlite3.connect("datos.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM usuarios WHERE id = {id_usuario}"
    cursor.execute(query)
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return jsonify({
            "id": resultado[0],
            "nombre": resultado[1],
            "clave": resultado[2],     # 🔍 este es clave
            "correo": resultado[3]
        })
    else:
        return jsonify({"error": "Usuario no encontrado"})


# ✅ REGISTRO
@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nuevo_usuario = request.form["username"]
        nueva_clave = request.form["password"]

        print(f"Registrando usuario: {nuevo_usuario}, clave: {nueva_clave}")  # <-- DEBUG

        conn = sqlite3.connect("datos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, clave) VALUES (?, ?)", (nuevo_usuario, nueva_clave))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("registro.html")

@app.route("/ver-usuarios")
def ver_usuarios():
    conn = sqlite3.connect("datos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    datos = cursor.fetchall()
    conn.close()
    return jsonify(datos)


# 🟩 BIENVENIDA
@app.route("/bienvenido")
def bienvenido():
    usuario = session.get("usuario")
    if not usuario:
        return redirect("/")
    return render_template("bienvenido.html", usuario=usuario)

# 🔁 CERRAR SESIÓN
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")

# 🟩 EJECUCIÓN
if __name__ == "__main__":
    app.run(debug=True)
