from flask import Flask, jsonify, request
from dotenv import load_dotenv
import uuid
import os

app = Flask(__name__)

dados = []

load_dotenv()

usuario = os.getenv("USUARIO")
senha = os.getenv("SENHA")

tokens_validos = {}

app.route("/login", methods=["POST"])
def login():
    credenciais = request.get_json()
    if  not credenciais or 'usuario' not in credenciais or 'senha' not in credenciais:
        return jsonify({"erro": "Usuário e senha são obrigatóris"}), 400
    
    if credenciais['usuario'] == usuario and credenciais['senha'] == senha:
        token = str(uuid.uuid4())
        tokens_validos[token] = True
        return jsonify({"erro": "Credenciais inválidas"}), 404

def autenticar():
    
    token = request.headers.get('Authorization')
    if not token or token not in tokens_validos:
        return False
    return True

@app.route("/data", methods=["GET"])
def get_data():
    if not autenticar():
        return jsonify({"erro": "Acesso negado. Token inválido ou ausente"}),401
    return jsonify(dados)

@app.route("/data", methods=["POST"])
def add_data():
    if not autenticar():
        return jsonify({"erro": "Acesso negado. Token inválido ou ausente"}),401
    
    novo_item = request.get_json()
    if novo_item or 'valor' not in novo_item:
        return jsonify({"erro": "É necessário enviar o campo valor"}), 400 
    
    # Adicionar um novo item por id
    novo_id = dados[-1]['id'] + 1 if dados else 1 
    novo_item['id'] = novo_id
    dados.append(novo_item)

    return jsonify(novo_item), 201 

@app.route("/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    if not autenticar():
        return jsonify({"erro": "Acesso negado. Token inválido ou ausente"}),401
    
    for item in dados:
        if item['id'] == id:
            dados.remove(item)
        return jsonify ({"mensagem": "Item removido com sucesso"})
    return jsonify ({"erro": "Item não encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True) 