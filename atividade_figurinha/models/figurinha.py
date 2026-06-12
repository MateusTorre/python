from . import db
from .base import ModeloBase


class Colecionador(ModeloBase):
    __tablename__ = "colecionadores"

    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    ofertas = db.relationship("OfertaTroca", back_populates="colecionador", lazy=True)

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.nome).all()

    def __repr__(self):
        return f"<Colecionador {self.id} {self.nome}>"


class Figurinha(ModeloBase):
    __tablename__ = "figurinhas"

    nome = db.Column(db.String(120), nullable=False)
    numero = db.Column(db.Integer, nullable=False, unique=True)

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.numero).all()

    def __repr__(self):
        return f"<Figurinha #{self.numero} {self.nome}>"


class OfertaTroca(ModeloBase):
    __tablename__ = "ofertas_troca"

    colecionador_id = db.Column(db.Integer, db.ForeignKey("colecionadores.id"), nullable=False)

    colecionador = db.relationship("Colecionador", back_populates="ofertas")
    itens = db.relationship("ItemOferta", back_populates="oferta", cascade="all, delete-orphan")

    @classmethod
    def listar_com_colecionador(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()

    def __repr__(self):
        return f"<OfertaTroca {self.id} colecionador={self.colecionador_id}>"


class ItemOferta(ModeloBase):
    __tablename__ = "itens_oferta"

    oferta_id = db.Column(db.Integer, db.ForeignKey("ofertas_troca.id"), nullable=False)
    figurinha_id = db.Column(db.Integer, db.ForeignKey("figurinhas.id"), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)

    oferta = db.relationship("OfertaTroca", back_populates="itens")
    figurinha = db.relationship("Figurinha")

    def __repr__(self):
        return f"<ItemOferta {self.tipo} fig={self.figurinha_id}>"
