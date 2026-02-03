from flask import Blueprint, session, jsonify
from src.application.usuario.ControleUsuario import ControleUsuario

usuario_bp = Blueprint("usuario", __name__)


# =========================
# Rotas de API (Estado diário)
# =========================

@usuario_bp.route("/api/usuario/status-diario", methods=["GET"])
def status_diario():
    """
    Retorna o estado de uso diário das funções:
    - cartas_diarias
    - fundicao
    - reforjar

    Regra:
    Se data_acao == hoje → BLOQUEADO
    Se data_acao < hoje ou NULL → DISPONÍVEL
    """

    if "usuario" not in session:
        return jsonify({
            "sucesso": False,
            "mensagem": "Não autenticado"
        }), 401

    nome = session["usuario"]["nome"]
    status = ControleUsuario().acoes_disponiveis(nome)

    if not status:
        return jsonify({
            "sucesso": False,
            "mensagem": "Usuário não encontrado"
        }), 404

    else:
        return jsonify({
            "sucesso": True,
            "data": status
        }), 200


# =========================
# Rotas de API (Marcar uso)
# =========================

@usuario_bp.route("/api/usuario/marcar-uso/<acao>", methods=["POST"])
def marcar_uso(acao):
    """
    ação ∈ { cartas_diarias, fundicao, reforjar }
    """

    if "usuario" not in session:
        return jsonify({"sucesso": False, "mensagem": "Não autenticado"}), 401

    nome = session["usuario"]["nome"]
    status = ControleUsuario().marcar_acao(nome, acao)

    if status == "Usuário não encontrado":
        return jsonify({
            "sucesso": False,
            "mensagem": "Usuário não encontrado"
        }), 404

    elif status == "Ação inválida":
        return jsonify({
            "sucesso": False,
            "mensagem": "Ação inválida"
        }), 400

    else:
        return jsonify({"sucesso": True})
