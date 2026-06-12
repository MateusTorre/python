# Esta pasta controllers/ exporta os Blueprints para o app.py registrar.
# Cada arquivo *_controller.py cria um Blueprint com nome único (ex: "clientes").
from controllers.clientes_controller import clientes_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.figurinhas_controller import figurinhas_bp
from controllers.pedidos_controller import pedidos_bp

__all__ = ["dashboard_bp", "clientes_bp", "figurinhas_bp", "pedidos_bp"]