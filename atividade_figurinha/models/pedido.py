from . import db
from .base import ModeloBase


class Pedido(ModeloBase):
    """Pedido principal — pertence a um Cliente (chave estrangeira)."""

    __tablename__ = "pedidos"

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="pendente")
    observacao = db.Column(db.String(255), nullable=True)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    itens = db.relationship(
        "ItemPedido", back_populates="pedido", cascade="all, delete-orphan"
    )

    # @property = "parece um atributo, mas calcula na hora"
    # Use: pedido.total   (SEM parênteses) — no template fica {{ pedido.total }}
    # Não guarda no banco; soma os itens toda vez que você pede.
    @property
    def total(self):
        return sum(item.subtotal for item in self.itens)

    @classmethod
    def listar_com_cliente(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()

    @classmethod
    def criar_com_itens(cls, cliente_id, itens_dados, observacao=""):
        pedido = cls(
            cliente_id=cliente_id,
            observacao=observacao or None,
            status="pendente",
        )
        db.session.add(pedido)
        db.session.flush()

        for item in itens_dados:
            db.session.add(
                ItemPedido(
                    pedido_id=pedido.id,
                    produto=item["produto"],
                    quantidade=item["quantidade"],
                    preco_unitario=item["preco_unitario"],
                )
            )
        db.session.commit()
        return pedido

    def __repr__(self):
        return f"<Pedido {self.id} cliente={self.cliente_id}>"


class ItemPedido(ModeloBase):
    """Itens do pedido — segunda tabela ligada a Pedido (FK)."""

    __tablename__ = "itens_pedido"

    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto = db.Column(db.String(120), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)

    pedido = db.relationship("Pedido", back_populates="itens")

    # @property de novo: quantidade * preço, sem chamar subtotal()
    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __repr__(self):
        return f"<ItemPedido {self.produto} x{self.quantidade}>"