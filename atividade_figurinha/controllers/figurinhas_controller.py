from flask import Blueprint, redirect, render_template, request, url_for
from models import Colecionador, Figurinha, ItemOferta, OfertaTroca, db


figurinhas_bp = Blueprint("figurinhas", __name__, url_prefix="/figurinhas")


@figurinhas_bp.route("/")
def index():
    ofertas = OfertaTroca.listar_com_colecionador()
    return render_template("figurinhas/lista_ofertas.html", ofertas=ofertas)


@figurinhas_bp.route("/oferta/cadastrar", methods=["GET", "POST"])
def cadastrar_oferta():
    colecionadores = Colecionador.listar()
    figurinhas = Figurinha.listar()

    if not colecionadores:
        return render_template(
            "figurinhas/formulario_oferta.html",
            colecionadores=[],
            figurinhas=figurinhas,
            erro="Cadastre um colecionador antes de criar ofertas.",
        )

    if request.method == "POST":
        colecionador_id = request.form.get("colecionador_id")

        if not colecionador_id or not db.session.get(Colecionador, colecionador_id):
            return render_template(
                "figurinhas/formulario_oferta.html",
                colecionadores=colecionadores,
                figurinhas=figurinhas,
                erro="Selecione um colecionador válido.",
            )

        oferecidas = request.form.getlist("figurinhas_oferecidas")
        desejadas = request.form.getlist("figurinhas_desejadas")

        if not oferecidas and not desejadas:
            return render_template(
                "figurinhas/formulario_oferta.html",
                colecionadores=colecionadores,
                figurinhas=figurinhas,
                erro="Selecione pelo menos uma figurinha para oferecer ou desejar.",
            )

        nova_oferta = OfertaTroca(colecionador_id=colecionador_id)
        db.session.add(nova_oferta)
        db.session.flush()

        for fig_id in oferecidas:
            db.session.add(ItemOferta(oferta_id=nova_oferta.id, figurinha_id=fig_id, tipo="oferece"))

        for fig_id in desejadas:
            db.session.add(ItemOferta(oferta_id=nova_oferta.id, figurinha_id=fig_id, tipo="deseja"))

        db.session.commit()
        return redirect(url_for("figurinhas.index"))

    return render_template(
        "figurinhas/formulario_oferta.html",
        colecionadores=colecionadores,
        figurinhas=figurinhas,
    )
