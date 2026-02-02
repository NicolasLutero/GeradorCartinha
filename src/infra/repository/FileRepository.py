from src.infra.database.FactoryConnection import FactoryConnection

import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename


class FileRepository:
    _instance = None

    BASE_DIR = Path(__file__).resolve().parent
    FILES_DIR = BASE_DIR / "files"
    TIPOS_VALIDOS = {"foto", "projeto"}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = FactoryConnection.get_connection()
        return cls._instance

    def save(self, arquivo, tipo: str) -> str:
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError("Tipo de arquivo inválido")

        if not arquivo or not arquivo.filename:
            raise ValueError("Arquivo inválido")

        # Gera UUID
        file_uuid = str(uuid.uuid4())

        # Preserva extensão original
        nome_seguro = secure_filename(arquivo.filename)
        extensao = os.path.splitext(nome_seguro)[1]

        # Diretório final
        diretorio = os.path.join(self.FILES_DIR, tipo)
        os.makedirs(diretorio, exist_ok=True)

        # Caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio, f"{file_uuid}{extensao}")

        # Salva o arquivo
        arquivo.save(caminho_arquivo)

        return file_uuid

    def load(self, file_uuid: str, tipo: str) -> str:
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError("Tipo de arquivo inválido")

        diretorio = os.path.join(self.FILES_DIR, tipo)

        if not os.path.isdir(diretorio):
            raise FileNotFoundError("Diretório não encontrado")

        for nome_arquivo in os.listdir(diretorio):
            if nome_arquivo.startswith(file_uuid):
                return os.path.join(diretorio, nome_arquivo)

        raise FileNotFoundError("Arquivo não encontrado")