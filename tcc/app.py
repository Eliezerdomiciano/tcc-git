from flask import Flask, render_template, request, jsonify
from flask_bcrypt import Bcrypt

import sqlite3


app = Flask(__name__)
app.config["SECRET_KEY"] = "Minha senha mais secreta possivel"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
bcrypt = Bcrypt(app)


# Conectando ao banco de dados SQLite
db = sqlite3.connect("my_database.db")
cursor = db.cursor()

# Crie a tabela para armazenar os dados do usuário
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        sobrenome TEXT,
        email TEXT,
        cpf TEXT,
        senha TEXT
    )
"""
)
db.commit()


# Criando um Class form


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/authenticate", methods=["POST"])
def authenticate():
    email = request.json.get("email")
    senha = request.json.get("senha")

    # Conecte-se ao banco de dados SQLite
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    # Consulte o banco de dados para verificar as credenciais
    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha)
    )
    user = cursor.fetchone()

    conn.close()

    if user:
        autenticado = True
    else:
        autenticado = False

    if autenticado:
        return "Login bem-sucedido"
    else:
        return "Falha no login"


@app.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastrar.html")


@app.route("/registration", methods=["POST"])
def registration():
    dados = request.json
    nome = dados["nome"]
    sobrenome = dados["sobrenome"]
    email = dados["email"]
    cpf = dados["cpf"]
    senha = dados["senha"]

    # Conecte ao banco de dados SQLite
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    # Insira os dados na tabela de usuários
    cursor.execute(
        "INSERT INTO usuarios (nome, sobrenome, email, cpf, senha) VALUES (?, ?, ?, ?, ?)",
        (nome, sobrenome, email, cpf, senha),
    )
    conn.commit()
    conn.close()

    return "Cadastro realizado com sucesso!"


@app.route("/stock", methods=["GET", "POST"])
def stock():
    if request.method == "POST":
        print("botão acionado")
        import scrapping as sp

        dados_produtos = sp.dados_produtos
        nome_arquivo = sp.pegandoMenorValor(dados_produtos)
        return jsonify({"arquivo.json": nome_arquivo})

    return render_template("estoque.html")


@app.route("/home")
def home():
    return render_template("principal.html")
