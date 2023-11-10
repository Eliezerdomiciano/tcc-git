from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    flash,
)

from flask_session import Session
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
    logout_user,
    UserMixin,
)
from flask_bcrypt import Bcrypt
from functools import wraps  # Importe 'wraps' para usar em decorações personalizadas


import sqlite3
import pandas as pd

# Resto do seu código

app = Flask(__name__)
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "MinhaChaveSecreta"
Session(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = "login"  # Defina a rota de login
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

# Conectando ao banco de dados SQLite
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# Crie a tabela para armazenar o histórico de produtos, se ainda não existir
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Historico (
        id INTEGER PRIMARY KEY,
        preco TEXT,
        fornecedor TEXT,
        nome_produto TEXT,
        link TEXT
    )
"""
)


db = sqlite3.connect("my_database.db")
cursor = db.cursor()

# Crie a tabela para recebimento de aparelhos
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS recebimento (
        id INTEGER PRIMARY KEY,
        modelo TEXT,
        nome_cliente TEXT,
        cpf_cliente TEXT,
        marca TEXT,
        data_recebida DATE,
        numero_serial TEXT
    )
    """
)


conn.commit()
conn.close()
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

        if user and bcrypt.check_password_hash(user[5], senha):
            # Login bem-sucedido: redirecionar para a página inicial
            login_user(User(user[0]))
            return redirect(url_for("home"))

        # Se a autenticação falhar, você pode exibir uma mensagem de erro com o Flash
        flash("Falha na autenticação. Usuário ou senha incorretos", "error")

    return render_template("login.html")


# Rota para fazer logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso", "success")
    return redirect(url_for("index"))


# @app.route("/authenticate", methods=["POST"])
# def authenticate():
#     email = request.json.get("email")
#     senha = request.json.get("senha")

#     # Conecte-se ao banco de dados SQLite
#     conn = sqlite3.connect("my_database.db")
#     cursor = conn.cursor()

#     # Consulte o banco de dados para verificar as credenciais
#     cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
#     user = cursor.fetchone()

#     if user and bcrypt.check_password_hash(user[5], senha):
#         print("Senha correta")
#         user_obj = User(user[0])
#         login_user(user_obj)
#         print("Usuário autenticado com sucesso")
#         return redirect(url_for("home"))
#     else:
#         print("Falha na autenticação. Usuário ou senha incorretos.")


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

    # Conecte-se ao banco de dados SQLite
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    # Crie o hash da senha
    senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

    # Insira os dados na tabela de usuários com a senha já hasheada
    cursor.execute(
        "INSERT INTO usuarios (nome, sobrenome, email, cpf, senha) VALUES (?, ?, ?, ?, ?)",
        (nome, sobrenome, email, cpf, senha_hash),
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


@app.route("/processar_upload_excel", methods=["POST"])
def processar_upload_excel():
    if "excel_file" not in request.files:
        # Lógica para lidar com o caso em que nenhum arquivo foi enviado
        return redirect(url_for("estoque"))

    file = request.files["excel_file"]

    if file.filename == "":
        # Lógica para lidar com o caso em que nenhum arquivo foi selecionado
        return redirect(url_for("estoque"))

    if file:
        # Lógica para processar o arquivo Excel
        df = pd.read_excel(file)

        # Aqui você deve manipular o DataFrame (df) e salvar os dados no banco de dados ou fazer outras operações necessárias

        # Exemplo de como imprimir o DataFrame (para fins de depuração)
        print(df)

    return redirect(url_for("estoque"))


# Rota para adicionar ao histórico
@app.route("/adicionar_ao_historico", methods=["POST"])
def adicionar_ao_historico():
    data = request.get_json()

    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Historico (preco, fornecedor, nome_produto, link) VALUES (?, ?, ?, ?)",
        (data["preco"], data["fornecedor"], data["nome"], data["link"]),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Dados adicionados ao histórico com sucesso"})


# Resto do seu código Flask


# Rota para a página principal (apenas acessível para usuários autenticados)
@app.route("/home")
@login_required
def home():
    if current_user.is_authenticated:
        print("Usuário autenticado. Acesso permitido.")
    else:
        print("Usuário não autenticado. Acesso negado.")
    return render_template("principal.html")


@app.route("/history")
@login_required
def history():
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Historico")
    historico_itens = cursor.fetchall()
    conn.close()

    return render_template("historico.html", historico_itens=historico_itens)


@app.route("/processar_upload", methods=["POST"])
@login_required
def processar_upload():
    if "excel_file" not in request.files:
        flash("Nenhum arquivo enviado", "error")
        return redirect("/receipt")

    file = request.files["excel_file"]

    if file.filename == "":
        flash("Nenhum arquivo selecionado", "error")
        return redirect("/receipt")

    if file:
        try:
            # Lógica para processar o arquivo Excel e inserir os dados na tabela recebimento
            df = pd.read_excel(file)

            conn = sqlite3.connect("my_database.db")
            cursor = conn.cursor()

            print("Dados lidos do DataFrame:")
            print(df)

            # Modifique a parte do código que lida com 'numero_serial'
            for index, row in df.iterrows():
                try:
                    # Convertendo o formato da data do Excel para o formato do banco de dados (dd-mm-yyyy)
                    data_recebida = pd.to_datetime(
                        row["data_recebida"], format="%d-%m-%Y"
                    ).strftime("%Y-%m-%d")

                    # Convertendo 'numero_Serial' para texto (TEXT)
                    numero_serial = str(row["numero_Serial"])

                    cursor.execute(
                        "INSERT INTO recebimento (modelo, nome_cliente, cpf_cliente, marca, data_recebida, numero_serial) VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            row["modelo"],
                            row["nome_cliente"],
                            row["cpf_cliente"],
                            row["marca"],
                            data_recebida,
                            numero_serial,
                        ),
                    )
                    print(f"Dados inseridos: {row}")
                except Exception as e:
                    print(f"Erro ao processar linha {index + 1} do arquivo: {str(e)}")

            conn.commit()  # Adicione esta linha para persistir as alterações no banco de dados
            flash("Upload e processamento bem-sucedidos", "success")
        except Exception as e:
            flash(f"Erro durante o processamento do arquivo: {str(e)}", "error")

    return redirect("/receipt")


@app.route("/recebimento")
@login_required
def receipt():
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recebimento")
    dados_recebimento = cursor.fetchall()

    return render_template("recebimento.html", dados_recebimento=dados_recebimento)


@app.route("/deletar_linha", methods=["POST"])
def deletar_linha():
    # Lógica para deletar a linha no banco de dados
    row_id = request.form.get("row_id")
    # ... (lógica de exclusão no banco de dados)
    return redirect("/receipt")  # ou para a página desejada


# Rota para adicionar equipamento
@app.route("/adicionar_equipamento", methods=["POST"])
@login_required
def adicionar_equipamento():
    dados_equipamento = request.json
    modelo = dados_equipamento["modelo"]
    nome_cliente = dados_equipamento["nome_cliente"]
    cpf_cliente = dados_equipamento["cpf_cliente"]
    marca = dados_equipamento["marca"]
    data_recebida = dados_equipamento["data_recebida"]
    numero_serial = dados_equipamento["numero_serial"]

    # Lógica para adicionar o equipamento no banco de dados
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recebimento (modelo, nome_cliente, cpf_cliente, marca, data_recebida, numero_serial) VALUES (?, ?, ?, ?, ?)",
        (modelo, nome_cliente, cpf_cliente, marca, data_recebida, numero_serial),
    )
    conn.commit()
    conn.close()

    return jsonify(
        {"status": "success", "message": "Equipamento adicionado com sucesso!"}
    )


@app.route("/about")
@login_required
def about():
    return render_template("sobre.html")


@app.route("/registration_equipament")
@login_required
def registration_equipament():
    return render_template("cadastrar_equip.html")


@app.route("/registration_products")
@login_required
def registration_products():
    return render_template("cadastrar_prod.html")


@app.route("/budget")
@login_required
def budget():
    return render_template("orcamento.html")


@app.route("/processar_aprovacao/<int:recebimento_id>/<status>", methods=["POST"])
@login_required
def processar_aprovacao(recebimento_id, status):
    # Lógica para processar a aprovação aqui (por exemplo, atualizar o status no banco de dados)

    # Redirecionar para a página de orçamento
    return redirect(url_for("budget"))


@app.route("/make_budget", methods=["POST"])
def make_budget():
    serial = request.form.get("serial")
    cliente = request.form.get("cliente")
    modelo = request.form.get("modelo")
    data_recebida = request.form.get("data_recebida")

    # Renderize a página 'realizar_orcamento.html' com os parâmetros necessários
    return render_template(
        "realizar_orcamento.html",
        serial=serial,
        cliente=cliente,
        modelo=modelo,
        data_recebida=data_recebida,
    )


@app.route("/orcar")
@login_required
def orcar():
    return render_template("orcar.html")


if __name__ == "__main__":
    app.secret_key = "your_secret_key_here"
    app.run(debug=True)
