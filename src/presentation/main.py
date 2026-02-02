from flask import Flask

from routes.SiteRoutes import site_bp
from routes.PedidoRoutes import pedido_bp


class Server(Flask):
    def __init__(self, import_name: str):
        super().__init__(
            import_name,
            template_folder="ui/templates",
            static_folder="ui/static"
        )
        self._registrar_rotas()
        self.pedidos = []

    def _registrar_rotas(self) -> None:
        # BluePrints
        self.register_blueprint(site_bp)
        self.register_blueprint(pedido_bp)


if __name__ == "__main__":
    app = Server(__name__)
    app.run(host="0.0.0.0", port=5050, debug=True)
