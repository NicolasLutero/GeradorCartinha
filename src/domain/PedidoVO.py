class PedidoVO:
    def __init__(self, pedido_id: int, cliente: str, con_telefone: str, con_email: str, tipo: str, outro: str, endereco: str, metragem: float, projetos, fotos):
        self._id = pedido_id
        self._cliente = cliente
        self._con_telefone = con_telefone
        self._con_email = con_email
        self._tipo = tipo
        self._outro = outro
        self._endereco = endereco
        self._metragem = metragem
        self._arq_projetos = projetos
        self._arq_fotos = fotos

    def get_id(self):
        return self._id

    def get_cliente(self):
        return self._cliente

    def get_telefone(self):
        return self._con_telefone

    def get_email(self):
        return self._con_email

    def get_tipo(self):
        return self._tipo

    def get_outro(self):
        return self._outro

    def get_endereco(self):
        return self._endereco

    def get_metragem(self):
        return self._metragem

    def set_id(self, novo_id):
        self._id = novo_id

    def set_cliente(self, cliente):
        self._cliente = cliente

    def set_whatsapp(self, whatsapp):
        self._con_whatsapp = whatsapp

    def set_email(self, email):
        self._con_email = email

    def set_tipo(self, tipo):
        self._tipo = tipo

    def set_outro(self, outro):
        self._outro = outro

    def set_endereco(self, endereco):
        self._endereco = endereco

    def set_metragem(self, metragem):
        self._metragem = metragem

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "cliente": self._cliente,
            "telefone": self._con_telefone,
            "email": self._con_email,
            "tipo": self._tipo,
            "outro": self._outro,
            "endereco": self._endereco,
            "metragem": self._metragem,
            "projetos": self._arq_projetos,
            "fotos": self._arq_fotos
        }

    @staticmethod
    def from_dict(dados) -> "PedidoVO":
        novo_id = -1
        if "id" in dados.keys():
            novo_id = dados["id"]
        cliente = dados["cliente"]
        con_telefone = dados["telefone"]
        con_email = dados["email"]
        tipo = dados["tipo"]
        outro = dados["outro"]
        endereco = dados["endereco"]
        metragem = dados["metragem"]
        arq_projetos = dados["projetos"]
        arq_fotos = dados["fotos"]
        return PedidoVO(novo_id, cliente, con_telefone, con_email, tipo, outro, endereco, metragem, arq_projetos, arq_fotos)
