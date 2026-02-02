from src.domain.PedidoVO import PedidoVO
from src.infra.dao.PedidoDAO import PedidoDAO
from src.infra.repository.FileRepository import FileRepository


class ControlePedido:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._pedidos = []
            cls._cache = {}
        return cls._instance

    # CREATE
    def adicionar_dict(self, pedido_dict: dict) -> None:
        pedido = PedidoVO.from_dict(pedido_dict)
        PedidoDAO().criar(pedido)
        self._cache[pedido.get_id()] = pedido

        for arq in pedido_dict["fotos"]:
            uuid_foto = FileRepository().save(arq["arquivo"], "foto")
            PedidoDAO().add_arquivo(pedido.get_id(), uuid_foto, "foto")

        for arq in pedido_dict["projetos"]:
            uuid_projeto = FileRepository().save(arq["arquivo"], "projeto")
            PedidoDAO().add_arquivo(pedido.get_id(), uuid_projeto, "projeto")

    # READ (ALL)
    def listar_dict(self) -> list:
        pedidos = []
        for pedido in PedidoDAO().listar_todos():
            if not pedido.get_id() in self._cache.keys():
                self._cache[pedido.get_id()] = pedido
            pedido = self._cache[pedido.get_id()].to_dict()
            pedido["qtd_projetos"] = len(pedido["projetos"])
            pedido["qtd_fotos"] = len(pedido["fotos"])
            del pedido["projetos"]
            del pedido["fotos"]
            pedidos.append(pedido)
        return pedidos

    # READ (ONE)
    def buscar_id_dict(self, pedido_id: int) -> dict | None:
        if pedido_id in self._cache.keys():
            return self._cache[pedido_id].to_dict()
        else:
            pedido = PedidoDAO().buscar_id(pedido_id)
            if pedido is not None:
                self._cache[pedido_id] = pedido
                return pedido.to_dict()
        return None

    # DELETE
    def deletar_id(self, pedido_id: int) -> bool:
        if PedidoDAO().deletar(pedido_id):
            self._cache.pop(pedido_id, None)
            return True
        return False

    def arquivos_pedido(self, pedido_id: int, tipo_arquivo: str) -> list[str]:
        if pedido_id in self._cache:
            pedido = self._cache[pedido_id]
        else:
            pedido = PedidoDAO().buscar_id(pedido_id)
            if pedido is None:
                raise ValueError("Pedido não encontrado")
            self._cache[pedido_id] = pedido
        pedido = pedido.to_dict()

        arquivos = []

        for file_uuid in pedido[tipo_arquivo + "s"]:
            caminho = FileRepository().load(file_uuid, tipo_arquivo)
            arquivos.append(caminho)

        return arquivos

    """
    # UPDATE
    def atualizar(self, pedido: dict) -> bool:
        pedido = PedidoVO.from_dict(pedido)
        return PedidoDAO().atualizar(pedido)
    """
