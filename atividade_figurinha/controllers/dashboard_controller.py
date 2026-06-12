from flask import Blueprint, render_template

from models import Cliente, Pedido

# Blueprint da home — sem url_prefix, então "/" é a raiz do site
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    return render_template(
        "index.html",
        total_clientes=Cliente.query.count(),
        total_pedidos=Pedido.query.count(),
        pedidos_recentes=Pedido.listar_com_cliente()[:5]
    )