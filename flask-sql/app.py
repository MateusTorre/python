import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)


pasta_aula = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    pasta_aula, "alunos.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.Int(20), nullable=False)

    def __repr__(self):
        return f"<Aluno {self.id} {self.nome}>"


with app.app_context():
    db.create_all()



@app.route("/")
def index():
    alunos = Aluno.query.order_by(Aluno.nome).all()
    return render_template("lista.html", alunos=alunos)



@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        if not nome or not email:
            return render_template(
                "formulario.html",
                titulo="Cadastrar aluno",
                erro="Preencha nome e e-mail.",
                nome=nome,
                email=email,
            )
        aluno = Aluno(nome=nome, email=email)
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("formulario.html", titulo="Cadastrar aluno")



@app.route("/editar/<int:aluno_id>", methods=["GET", "POST"])
def editar(aluno_id):
    aluno = db.session.get(Aluno, aluno_id)
    if not aluno:
        return redirect(url_for("index"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        if not nome or not email:
            return render_template(
                "formulario.html",
                titulo="Editar aluno",
                erro="Preencha nome e e-mail.",
                nome=nome,
                email=email,
                aluno_id=aluno.id,
            )
        aluno.nome = nome
        aluno.email = email
        db.session.commit()
        return redirect(url_for("index"))

    return render_template(
        "formulario.html",
        titulo="Editar aluno",
        nome=aluno.nome,
        email=aluno.email,
        aluno_id=aluno.id,
    )


@app.route("/excluir/<int:aluno_id>", methods=["POST"])
def excluir(aluno_id):
    aluno = db.session.get(Aluno, aluno_id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
