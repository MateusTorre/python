from flask import Blueprint, redirect, render_template, request, url_for

from models import Cliente, Pedido, db

# Outro Blueprint, outro "módulo" de rotas — mesmo app, pasta mental separada (pedidos)
# No HTML: url_for('pedidos.listar') — primeiro nome é o Blueprint, segundo é a função
pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")

def _ler_itens_form():
    produtos = request.form.getlist("produto")
    quantidades = request.form.getlist("quantidade")
    precos = request.form.getlist("preco_unitario")
    itens = []
    for produto, qtd, preco in zip(produtos, quantidades, precos):
        produto = produto.strip()
        if not produto:
            continue
        try:
            itens.append(
                {
                    "produto": produto,
                    "quantidade": int(qtd),
                    "preco_unitario": float(str(preco).replace(",", ".")),
                }
            )
        except ValueError:
            return None, "Quantidade ou preço inválido nos itens."
    if not itens:
        return None, "Adicione pelo menos um item ao pedido."
    return itens, None


# Decorator @route: GET em /pedidos/ chama esta função
@pedidos_bp.route("/")
def listar():
    return render_template(
        "pedidos/lista.html", pedidos=Pedido.listar_com_cliente()
    )


@pedidos_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    clientes = Cliente.listar_ordenados()
    if not clientes:
        return render_template(
            "pedidos/formulario.html",
            titulo="Novo pedido",
            clientes=[],
            erro="Cadastre um cliente antes de criar pedidos.",
        )

    if request.method == "POST":
        try:
            cliente_id = int(request.form.get("cliente_id", 0))
        except ValueError:
            cliente_id = 0
        observacao = request.form.get("observacao", "").strip()
        itens, erro_itens = _ler_itens_form()

        if not cliente_id or not db.session.get(Cliente, cliente_id):
            erro = "Selecione um cliente válido."
        elif erro_itens:
            erro = erro_itens
        else:
            # @classmethod — monta pedido + itens num lugar só
            Pedido.criar_com_itens(cliente_id, itens, observacao)
            return redirect(url_for("pedidos.listar"))
        return render_template(
            "pedidos/formulario.html",
            titulo="Novo pedido",
            clientes=clientes,
            erro=erro,
            observacao=observacao,
        )

    return render_template(
        "pedidos/formulario.html", titulo="Novo pedido", clientes=clientes
    )


@pedidos_bp.route("/<int:pedido_id>")
def detalhe(pedido_id):
    pedido = db.session.get(Pedido, pedido_id)
    if not pedido:
        return redirect(url_for("pedidos.listar"))
    return render_template("pedidos/detalhe.html", pedido=pedido)