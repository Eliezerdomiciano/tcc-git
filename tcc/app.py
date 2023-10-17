from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_session import Session
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user,
    UserMixin,
)
from flask_bcrypt import Bcrypt

import sqlite3


app = Flask(__name__)
# Configuração da extensão Flask-Session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "MinhaChaveSecreta"
Session(app)
bcrypt = Bcrypt(app)

# Adicione as configurações do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(id):
    return User(id)


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


# Middleware para proteger rotas
def proteger_rotas(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        # Verifique as credenciais do usuário no banco de dados
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[4], senha):
            user_obj = User(user[0])
            login_user(user_obj)
            return redirect(url_for("home"))

    return render_template("login.html")


# Rota para fazer logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/authenticate", methods=["POST"])
def authenticate():
    email = request.json.get("email")
    senha = request.json.get("senha")

    # Conecte-se ao banco de dados SQLite
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    # Consulte o banco de dados para verificar as credenciais
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user[4], senha):
        autenticado = True
    else:
        autenticado = False

    conn.close()

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
@login_required
def stock():
    if request.method == "POST":
        print("botão acionado")
        import scrapping as sp

        dados_produtos = sp.dados_produtos
        nome_arquivo = sp.pegandoMenorValor(dados_produtos)
        return jsonify({"arquivo.json": nome_arquivo})

    return render_template("estoque.html")


# Rota para a página principal (apenas acessível para usuários autenticados)
@app.route("/home")
@login_required
def home():
    return render_template("principal.html")
