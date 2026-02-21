# InventarioUserCace.py

# Domain Class
from src.domain.service.UsuarioService import UsuarioService
from src.domain.service.CartaService import CartaService

# Exception
from src.application.exception.ApplicationException import *


class InventarioUserCase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.usuario_service = UsuarioService()
            cls.carta_service = CartaService()
        return cls._instance

    # -------------------------------------------
    # LISTAR TIPOS DE FUNDO, PERSONAGEM E BORDA
    # -------------------------------------------
    def buscar_tipos(self, usuario) -> list[str]:
        usuario = self.usuario_service.buscar_usuario(usuario)
        return self.usuario_service.listar_tipos(usuario)


    # -------------------------------------------
    # BUSCAR CARTAS DO USUÁRIO
    # -------------------------------------------
    def buscar_cartas_usuario(self, usuario: str, tipos: dict) -> list[dict]:
        usuario = self.usuario_service.buscar_usuario(usuario)

        if usuario is None:
            raise UsuarioNaoExisteException()

        id_usuario = usuario.get_id()
        cartas_entities = self.usuario_service.buscar_cartas_filtrado(id_usuario, tipos)

        return [self.carta_service.para_client(carta) for carta in cartas_entities]


    # -------------------------------------------
    # BUSCAR CARTA ESPECÍFICA DO USUÁRIO
    # -------------------------------------------
    def buscar_carta_usuario(self, usuario: str, id_carta: int) -> dict:
        usuario = self.usuario_service.buscar_usuario(usuario)
        if usuario is None:
            raise UsuarioNaoExisteException()

        carta = self.carta_service.buscar_carta(id_carta)
        if carta is None:
            raise CartaNaoExisteException()

        id_usuario = usuario.get_id()
        dono_carta = carta.get_dono()
        if id_usuario != dono_carta:
            raise CartaNaoPertenceAOUsuarioException()

        return self.carta_service.para_client(carta)

    # -------------------------------------------
    # COLETAR CARTAS
    # -------------------------------------------
    def coletar_cartas(self, nome):
        usuario = self.usuario_service.buscar_usuario(nome)
        if not usuario:
            raise UsuarioNaoExisteException()

        self.usuario_service.verifica_status(usuario, ["cartas_diarias"])
        cartas = self.carta_service.gerar_n_cartas(5, usuario)
        self.usuario_service.marcar_acao(usuario, "cartas_diarias")

        return [self.carta_service.para_client(carta) for carta in cartas]

    # -------------------------------------------
    # REFORJAR CARTA
    # -------------------------------------------
    def reforjar_carta(self, nome_usuario, id_carta):
        usuario = self.usuario_service.buscar_usuario(nome_usuario)
        if not usuario:
            raise UsuarioNaoExisteException()

        carta = self.carta_service.buscar_carta(id_carta)
        if carta is None:
            raise CartaNaoExisteException()

        id_usuario = usuario.get_id()
        dono_carta = carta.get_dono()
        if id_usuario != dono_carta:
            raise CartaNaoPertenceAOUsuarioException()

        self.usuario_service.verifica_status(usuario, ["reforjar"])
        carta_reforjada = self.carta_service.reforjar(usuario, carta)
        self.usuario_service.marcar_acao(usuario, ["reforjar"])

        return self.carta_service.para_client(carta_reforjada)


    # -------------------------------------------
    # FUNDIR CARTAS
    # -------------------------------------------
    def fundir_cartas(self, nome_usuario, id_carta_base, id_carta_sacrificio):
        usuario = self.usuario_service.buscar_usuario(nome_usuario)
        if not usuario:
            raise UsuarioNaoExisteException()

        carta_base = self.carta_service.buscar_carta(id_carta_base)
        carta_sacrificio = self.carta_service.buscar_carta(id_carta_sacrificio)
        if carta_base is None or carta_sacrificio is None:
            raise CartaNaoExisteException()

        id_usuario = usuario.get_id()
        dono_carta_base = carta_base.get_dono()
        dono_carta_sacrificio = carta_sacrificio.get_dono()
        if not (id_usuario == dono_carta_base == dono_carta_sacrificio):
            raise CartaNaoPertenceAOUsuarioException()

        self.usuario_service.verifica_status(usuario, ["fundir"])
        carta_fundida = self.carta_service.fundir(carta_base, carta_sacrificio)
        self.usuario_service.marcar_acao(usuario, ["fundicao"])

        return self.carta_service.para_client(carta_fundida)
