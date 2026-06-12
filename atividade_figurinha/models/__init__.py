# Aqui nasce o "db" — é ele que conversa com o arquivo .db do SQLite.
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# O PONTO (.) no import = "pega da MESMA pasta models/"
# Ex.: from .cliente = arquivo cliente.py que está do seu lado, no mesmo apartamento.
# Já no controller a gente usa "from models import Cliente" (sem ponto) porque olhamos de FORA.
from .base import ModeloBase
from .cliente import Cliente
from .figurinha import Colecionador, Figurinha, ItemOferta, OfertaTroca
from .pedido import ItemPedido, Pedido

__all__ = [
    "db", "ModeloBase",
    "Cliente", "Colecionador", "Figurinha", "ItemOferta", "ItemPedido", "OfertaTroca", "Pedido",
]