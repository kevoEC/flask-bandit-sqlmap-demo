from flask import Flask, render_template, request, redirect, jsonify
import os
import sqlite3

app = Flask(__name__)

# 🟩 RUTA PRINCIPAL – LOGIN VULNERABLE (Bandit)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["username"]
        password = request.form["password"]

        # 🔥 Vulnerabilidad: log de contraseñas en texto plano
        with open("log.txt", "a") as f:
            f.write(f"{usuario}:{password}\n")

        # 🔥 Vulnerabilidad: comando shell sin sanitizar
        os.system("echo " + usuario)

        # Simula autenticación exitosa
        return redirect("/bienvenido")

    return render_template("login.html")

# 🟩 RUTA DE BIENVENIDA
@app.route("/bienvenido")
def bienvenido():
    return "<h1>Bienvenido al sistema</h1>"

# 🟥 RUTA VULNERABLE PARA SQLMAP
@app.route("/buscar")
def buscar_usuario():
    id_usuario = request.args.get("id")

    # 🔥 Vulnerabilidad SQL Injection directa (sin parámetros seguros)
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
            "correo": resultado[2]
        })
    else:
        return jsonify({"error": "Usuario no encontrado"})

# 🟩 CORRER SERVIDOR
if __name__ == "__main__":
    app.run(debug=True)
