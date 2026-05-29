import math
from flask import render_template, request

def calcular():
    num1 = float(request.form["num1"])
    operacao = request.form["operacao"]
    
  
    if operacao == "sqrt":
        if num1 < 0:
            resultado = "Erro: número negativo"
            etapas = f"Não existe raiz real de {num1}."
        else:
            resultado = math.sqrt(num1)
            etapas = f"√{num1} = {resultado}"
             
   
    elif operacao == "baskara":
        num2_valor = request.form.get("num2", "").strip()
        num3_valor = request.form.get("num3", "").strip()
        
     
        if not num2_valor or not num3_valor:
            return render_template(
                "calculadora.html", 
                etapas="Informe o segundo (B) e o terceiro (C) número para Bhaskara.", 
                resultado=""
            )
            
        num2 = float(num2_valor)
        num3 = float(num3_valor)
        
        if num1 == 0:
            resultado = "Erro: 'A' não pode ser 0"
            etapas = "Em uma equação do 2º grau, o coeficiente 'A' deve ser diferente de zero."
        else:
            delta = (num2 ** 2) - (4 * num1 * num3)
            etapas = f"Δ = {num2}² - 4 * {num1} * {num3} = {delta}"
            
            if delta < 0:
                resultado = "Sem raízes reais"
                etapas += " | Como Δ < 0, a equação não possui raízes reais."
            elif delta == 0:
                x = -num2 / (2 * num1)
                resultado = f"X = {x}"
                etapas += f" | Raiz única: X = -({num2}) / (2 * {num1})"
            else:
                x1 = (-num2 + math.sqrt(delta)) / (2 * num1)
                x2 = (-num2 - math.sqrt(delta)) / (2 * num1)
                resultado = f"X' = {x1} e X'' = {x2}"
                etapas += f" | Raízes: X = (-({num2}) ± √{delta}) / (2 * {num1})"

    else:
        num2_valor = request.form.get("num2", "").strip()
        if not num2_valor:
            return render_template(
                "calculadora.html", 
                etapas="Informe o segundo número para esta operação.", 
                resultado=""
            )
        
        num2 = float(num2_valor)
        
        if operacao == "+":
            resultado = num1 + num2
            etapas = f"{num1} + {num2} = {resultado}"
            
        elif operacao == "-":
            resultado = num1 - num2
            etapas = f"{num1} - {num2} = {resultado}"
            
        elif operacao == "*":
            resultado = num1 * num2
            etapas = f"{num1} * {num2} = {resultado}"
            
        elif operacao == "/":
            if num2 != 0:
                resultado = num1 / num2
                etapas = f"{num1} / {num2} = {resultado}"
            else:
                resultado = "ERRO: não se pode dividir um número por 0"
                etapas = "Não se pode dividir um número por 0"
                
        elif operacao == "**":
            resultado = num1 ** num2
            etapas = f"{num1} ** {num2} = {resultado}"
            
        elif operacao == "log":
            
            if num1 <= 0:
                resultado = "Erro matemático"
                etapas = "O logaritmando (Primeiro número) deve ser maior que 0."
            elif num2 <= 0 or num2 == 1:
                resultado = "Erro matemático"
                etapas = "A base (Segundo número) deve ser maior que 0 e diferente de 1."
            else:
                resultado = math.log(num1, num2)
                etapas = f"log de {num1} na base {num2} = {resultado}"
            
        else:
            resultado = "Operação errada!"
            etapas = "Operação errada!"
            
    return render_template("calculadora.html", etapas=etapas, resultado=resultado)
