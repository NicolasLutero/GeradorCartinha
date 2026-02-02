from src.application.pedido.ControlePedido import ControlePedido

import os
import tempfile
import zipfile

from flask import Blueprint, request, jsonify, abort, send_file


pedido_bp = Blueprint("controle_pedidos", __name__)


@pedido_bp.route("/criar_pedido", methods=["POST"])
def criar_pedido():
    dados = request.form

    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    tipo = dados.get("tipo")
    outro = dados.get("outro", "")

    if tipo == "Outro" and not outro:
        return jsonify({"erro": "Campo 'outro' obrigatório quando tipo é Outro"}), 400

    pedido = {
        "cliente": dados.get("cliente"),
        "telefone": dados.get("telefone"),
        "email": dados.get("email"),
        "tipo": tipo,
        "outro": outro if tipo == "Outro" else "",
        "endereco": dados.get("endereco"),
        "metragem": dados.get("metragem"),
        "projetos": [],
        "fotos": []
    }

    arquivos_projetos = request.files.getlist("arq_projetos")
    arquivos_fotos = request.files.getlist("arq_fotos")

    for arquivo in arquivos_projetos:
        pedido["projetos"].append({
            "filename": arquivo.filename,
            "content_type": arquivo.content_type,
            "arquivo": arquivo
        })

    for arquivo in arquivos_fotos:
        pedido["fotos"].append({
            "filename": arquivo.filename,
            "content_type": arquivo.content_type,
            "arquivo": arquivo
        })

    ControlePedido().adicionar_dict(pedido)
    del pedido["fotos"]
    del pedido["projetos"]

    return jsonify({
        "status": "criado",
        "pedido": pedido
    }), 201


@pedido_bp.route("/listar_pedidos", methods=["GET"])
def listar_pedidos():
    pedidos = ControlePedido().listar_dict()
    return jsonify(pedidos), 200

@pedido_bp.route("/download_arquivos/<int:pedido_id>/<string:tipo_arquivo>", methods=["GET"])
def download_arquivos(pedido_id: int, tipo_arquivo: str):
    try:
        arquivos = ControlePedido().arquivos_pedido(pedido_id, tipo_arquivo)

        if not arquivos:
            abort(404, description="Nenhum arquivo encontrado")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zipf:
                for caminho in arquivos:
                    nome = os.path.basename(caminho)
                    zipf.write(caminho, arcname=nome)

        return send_file(
            tmp.name,
            as_attachment=True,
            download_name=f"{tipo_arquivo}_{pedido_id}.zip"
        )

    except ValueError as e:
        abort(404, description=str(e))
    except FileNotFoundError as e:
        abort(404, description=str(e))

@pedido_bp.route("/buscar_pedido/<int:pedido_id>", methods=["GET"])
def buscar_pedido(pedido_id: int):
    pedido = ControlePedido().buscar_id_dict(pedido_id)
    if pedido is not None:
        return jsonify(pedido), 200
    return jsonify({"erro": "Pedido não encontrado"}), 404

@pedido_bp.route("/deletar_pedido/<int:pedido_id>", methods=["DELETE"])
def deletar_pedido(pedido_id: int):
    if ControlePedido().deletar_id(pedido_id):
        return jsonify({"status": "deletado", "id": pedido_id}), 200
    return jsonify({"erro": "ID inválido"}), 400
