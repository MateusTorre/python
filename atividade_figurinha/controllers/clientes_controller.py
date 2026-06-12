from flask import Blueprint, redirect, render_template, request, url_for

from models import Cliente, db

# BLUEPRINT = agrupador de rotas com apelido "clientes"
# url_for('clientes.listar') | URLs começam com /clientes/
clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@clientes_bp.route("/")
def listar():
    return render_template("clientes/lista.html", clientes=Cliente.listar_ordenados())


@clientes_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        if not nome or not email:
            return render_template(
                "clientes/formulario.html",
                titulo="Cadastrar cliente",
                erro="Nome e e-mail são obrigatórios.",
                nome=nome,
                email=email,
                telefone=telefone,
            )
        Cliente.salvar(nome, email, telefone)
        return redirect(url_for("clientes.listar"))

    return render_template("clientes/formulario.html", titulo="Cadastrar cliente")


@clientes_bp.route("/editar/<int:cliente_id>", methods=["GET", "POST"])
def editar(cliente_id):
    cliente = db.session.get(Cliente, cliente_id)
    if not cliente:
        return redirect(url_for("clientes.listar"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        if not nome or not email:
            return render_template(
                "clientes/formulario.html",
                titulo="Editar cliente",
                erro="Nome e e-mail são obrigatórios.",
                nome=nome,
                email=email,
                telefone=telefone,
                cliente_id=cliente.id,
            )
        cliente.atualizar(nome, email, telefone)
        return redirect(url_for("clientes.listar"))

    return render_template(
        "clientes/formulario.html",
        titulo="Editar cliente",
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone or "",
        cliente_id=cliente.id,
    )


@clientes_bp.route("/excluir/<int:cliente_id>", methods=["POST"])
def excluir(cliente_id):
    cliente = db.session.get(Cliente, cliente_id)
    if cliente:
        cliente.excluir()
    return redirect(url_for("clientes.listar"))