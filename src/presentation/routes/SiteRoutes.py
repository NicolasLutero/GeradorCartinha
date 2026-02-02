from flask import Blueprint, render_template

site_bp = Blueprint("site", __name__)

@site_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@site_bp.route("/pagina-criar-pedido", methods=["GET"])
def pagina_pedido():
    return render_template("criar_pedido.html")

@site_bp.route("/pagina-listar-pedido", methods=["GET"])
def pagina_listar_pedido():
    return render_template("listar_pedidos.html")
