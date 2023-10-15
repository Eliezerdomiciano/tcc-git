from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
app.config["SECRET_KEY"] = "Minha senha mais secreta possivel"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


# Criando um Class form


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/registration")
def registration():
    return render_template("cadastrar.html")


@app.route("/stock", methods=["GET", "POST"])
def stock():
    if request.method == "POST":
        print("botão acionado")
        import scrapping as sp

        # Obtendo Dados
        dados_produtos = sp.obter_dados_produtos

        nome_arquivo = sp.pegandoMenorValor(dados_produtos)
        print(nome_arquivo)
        return jsonify({"arquivo.json": nome_arquivo})

    return render_template("estoque.html")


@app.route("/home")
def home():
    return render_template("principal.html")
