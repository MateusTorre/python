from flask import Flask, request, render_template_string


app = Flask(__name__)

usuarios_permitidos = [ 

    {"usuario": "Marcos", "senha": "cotemig2026"},
    {"usuario": "janaína", "senha": "cotemig2026"},
    {"usuario": "Mateus", "senha": "12402150"}
]
   

def show_the_login_form():
    return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            <input type="text" name="usuario" placeholder="Usuário"><br><br>
            <input type="password" name="senha" placeholder="Senha"><br><br>
            <button type="submit">Entrar</button>
        </form>
    """)

def do_the_login():

    usuarios_inserido = request.form.get('usuario')
    senha_inserida = request.form.get('senha')

   for credencial in usuarios_permitidos:
        if credencial ["usuario"] == usuarios_inserido and credencial ["senha"] == senha_inserida:
        return f"<h1Bem-Vindo, {usuarios_inserido}</h1>"

    return "<h1>Lgin Invalido </h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

if __name__ == "__main__":
    app.run(debug=True)

    