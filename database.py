import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_file = 'autofill.db'
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Criar tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    telefone TEXT,
                    cpf TEXT UNIQUE,
                    endereco TEXT,
                    cidade TEXT,
                    estado TEXT,
                    cep TEXT,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP
                )
            ''')
            
            # Criar tabela de histórico de preenchimento
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_preenchimento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    site_url TEXT,
                    data_preenchimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sucesso BOOLEAN,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')
            
            conn.commit()

    def salvar_usuario(self, dados):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Verificar se o usuário já existe (por email ou CPF)
            cursor.execute('SELECT id FROM usuarios WHERE email = ? OR cpf = ?', 
                         (dados['email'], dados['cpf']))
            usuario_existente = cursor.fetchone()
            
            if usuario_existente:
                # Atualizar usuário existente
                cursor.execute('''
                    UPDATE usuarios 
                    SET nome = ?, telefone = ?, endereco = ?, 
                        cidade = ?, estado = ?, cep = ?,
                        data_atualizacao = ?
                    WHERE id = ?
                ''', (
                    dados['nome'], dados['telefone'], dados['endereco'],
                    dados['cidade'], dados['estado'], dados['cep'],
                    datetime.now(), usuario_existente[0]
                ))
                return usuario_existente[0]
            else:
                # Inserir novo usuário
                cursor.execute('''
                    INSERT INTO usuarios (
                        nome, email, telefone, cpf, endereco, 
                        cidade, estado, cep, data_atualizacao
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    dados['nome'], dados['email'], dados['telefone'],
                    dados['cpf'], dados['endereco'], dados['cidade'],
                    dados['estado'], dados['cep'], datetime.now()
                ))
                return cursor.lastrowid

    def carregar_usuario(self, email=None, cpf=None):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            if email:
                cursor.execute('''
                    SELECT nome, email, telefone, cpf, endereco, 
                           cidade, estado, cep 
                    FROM usuarios 
                    WHERE email = ?
                ''', (email,))
            elif cpf:
                cursor.execute('''
                    SELECT nome, email, telefone, cpf, endereco, 
                           cidade, estado, cep 
                    FROM usuarios 
                    WHERE cpf = ?
                ''', (cpf,))
            else:
                return None
                
            resultado = cursor.fetchone()
            if resultado:
                return {
                    'nome': resultado[0],
                    'email': resultado[1],
                    'telefone': resultado[2],
                    'cpf': resultado[3],
                    'endereco': resultado[4],
                    'cidade': resultado[5],
                    'estado': resultado[6],
                    'cep': resultado[7]
                }
            return None

    def registrar_preenchimento(self, usuario_id, site_url, sucesso):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO historico_preenchimento (
                    usuario_id, site_url, sucesso
                ) VALUES (?, ?, ?)
            ''', (usuario_id, site_url, sucesso)) 