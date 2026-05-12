from flask import Flask

app = Flask(__name__) 


@app.route('/decorator') 
def ola_mundo():
    return '''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Currículo</title>
        </head>
        <body>
            <h1>O que é um decorator?</h1>

         Decoradores (decorators) em Python são funções que modificam ou aprimoram o comportamento de outras funções ou métodos sem alterar seu código-fonte original
    
    </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
