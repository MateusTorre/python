import os

from flask import Flask

# Cada "bp" importado é um Blueprint — um pacote de rotas (clientes, pedidos, etc.)
from controllers import clientes_bp, dashboard_bp, figurinhas_bp, pedidos_bp
from models import Cliente, ItemPedido, Pedido, db


def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "pedidos.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # BLUEPRINT — explicação rápida:
    # Em vez de jogar TODAS as rotas aqui no app.py, cada assunto fica no seu controller.
    # register_blueprint = "liga" esse pacote de rotas ao Flask (tipo plugar um módulo no jogo).
    # clientes_bp → URLs começam com /clientes
    # pedidos_bp  → URLs começam com /pedidos
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(figurinhas_bp)
    app.register_blueprint(pedidos_bp)


    with app.app_context():
        db.create_all()

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)