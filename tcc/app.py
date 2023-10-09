from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


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


@app.route("/stock")
def stock():
    return render_template("estoque.html")


@app.route("/about")
def about():
    return render_template("sobre.html")
