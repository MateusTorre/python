from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = "chave_secreta"

def conectar():
    return sqlite3.connect("banco.db")

def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        status TEXT,
        usuario_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

criar_banco()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = generate_password_hash(request.form["senha"])

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuarios(nome,email,senha) VALUES(?,?,?)",
                (nome,email,senha)
            )
            conn.commit()
            flash("Cadastro realizado!")
            return redirect("/login")

        except:
            flash("Email já cadastrado!")

        conn.close()

    return render_template("cadastro.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=?",
            (email,)
        )

        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario[3], senha):
            session["usuario_id"] = usuario[0]
            session["nome"] = usuario[1]
            return redirect("/dashboard")

        flash("Login inválido!")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/dashboard")
def dashboard():

    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tarefas WHERE usuario_id=?",
        (session["usuario_id"],)
    )

    tarefas = cursor.fetchall()

    frase = ""

    try:
        resposta = requests.get("https://api.adviceslip.com/advice")
        frase = resposta.json()["slip"]["advice"]
    except:
        frase = "Tenha um ótimo dia!"

    return render_template(
        "dashboard.html",
        tarefas=tarefas,
        frase=frase
    )

@app.route("/nova_tarefa", methods=["GET","POST"])
def nova_tarefa():

    if "usuario_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        status = request.form["status"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tarefas
        (titulo,descricao,status,usuario_id)
        VALUES(?,?,?,?)
        """,
        (
            titulo,
            descricao,
            status,
            session["usuario_id"]
        ))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("nova_tarefa.html")

@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        status = request.form["status"]

        cursor.execute("""
        UPDATE tarefas
        SET titulo=?,
            descricao=?,
            status=?
        WHERE id=?
        """,
        (titulo,descricao,status,id))

        conn.commit()

        return redirect("/dashboard")

    cursor.execute(
        "SELECT * FROM tarefas WHERE id=?",
        (id,)
    )

    tarefa = cursor.fetchone()

    return render_template(
        "editar_tarefa.html",
        tarefa=tarefa
    )

@app.route("/excluir/<int:id>")
def excluir(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tarefas WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)