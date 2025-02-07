from flask import Flask, render_template, request, jsonify, session
import json
import os
from auto_preenchimento import AutoPreenchimento
from database import Database
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Importante para sessões
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salvar_dados', methods=['POST'])
def salvar_dados():
    try:
        dados = request.get_json()
        
        # Salvar no banco de dados
        usuario_id = db.salvar_usuario(dados)
        
        # Guardar email na sessão para identificar o usuário
        session['user_email'] = dados['email']
        
        return jsonify({
            "message": "Dados salvos com sucesso!",
            "usuario_id": usuario_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/carregar_dados')
def carregar_dados():
    try:
        # Tentar carregar dados usando email da sessão
        email = session.get('user_email')
        if email:
            dados = db.carregar_usuario(email=email)
            if dados:
                return jsonify(dados)
        return jsonify({})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/iniciar_preenchimento')
def iniciar_preenchimento():
    try:
        email = session.get('user_email')
        if not email:
            return jsonify({"error": "Usuário não identificado"}), 401
            
        dados = db.carregar_usuario(email=email)
        if not dados:
            return jsonify({"error": "Dados não encontrados"}), 404
            
        auto = AutoPreenchimento()
        auto.dados_pessoais = dados
        
        # Registrar tentativa de preenchimento
        usuario_id = db.salvar_usuario(dados)  # Isso retorna o ID do usuário
        site_url = request.args.get('url', 'URL não especificada')
        db.registrar_preenchimento(usuario_id, site_url, True)
        
        return jsonify({"message": "Preenchimento automático iniciado"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Define a porta 5000 e permite acesso externo (host='0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 