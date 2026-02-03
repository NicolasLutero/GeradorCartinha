# SiteRoutes.py
from flask import Blueprint, render_template

site_bp = Blueprint("site", __name__)

# --- Autenticação ---
@site_bp.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@site_bp.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastro.html")

# --- Home ---
@site_bp.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

# --- Funcionalidades ---
@site_bp.route("/cartas_diarias", methods=["GET"])
def cartas_diarias():
    return render_template("cartas_diarias.html")

@site_bp.route("/fundicao", methods=["GET"])
def fundicao():
    return render_template("fundicao.html")

@site_bp.route("/reforjar", methods=["GET"])
def reforjar():
    return render_template("reforjar.html")
