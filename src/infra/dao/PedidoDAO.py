from src.domain.PedidoVO import PedidoVO
from src.infra.database.FactoryConnection import FactoryConnection


class PedidoDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = FactoryConnection.get_connection()
        return cls._instance

    def next_id(self):
        sql = """
            SELECT COALESCE(MAX(id), 0)
            FROM pedido
        """
        with self._conn.cursor() as cur:
            cur.execute(sql)
            resultado = cur.fetchone()
        return resultado[0] + 1

    # CREATE
    def criar(self, pedido: PedidoVO) -> None:
        sql = """
            INSERT INTO pedido (id, nome_cliente, email, numero, tipo_servico, outro, endereco, metragem)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        novo_id = self.next_id()

        with self._conn.cursor() as cur:
            cur.execute(sql, (
                novo_id,
                pedido.get_cliente(),
                pedido.get_email(),
                pedido.get_telefone(),
                pedido.get_tipo(),
                pedido.get_outro(),
                pedido.get_endereco(),
                pedido.get_metragem()
            ))
        self._conn.commit()
        pedido.set_id(novo_id)

    # READ ALL
    def listar_todos(self) -> list[PedidoVO]:
        sql = """
            SELECT id, nome_cliente, email, numero, tipo_servico, outro, endereco, metragem
            FROM pedido
            WHERE deletado = FALSE
            ORDER BY id
        """

        with self._conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

        return [
            PedidoVO(
                pedido_id=row[0],
                cliente=row[1],
                con_email=row[2],
                con_telefone=row[3],
                tipo=row[4],
                outro=row[5],
                endereco=row[6],
                metragem=row[7],
                projetos=self.listar_arquivos_por_tipo(row[0], "projeto"),
                fotos=self.listar_arquivos_por_tipo(row[0], "foto")
            )
            for row in rows
        ]

    # READ ONE
    def buscar_id(self, pedido_id: int) -> PedidoVO | None:
        sql = """
            SELECT id, nome_cliente, email, numero, tipo_servico, outro, endereco, metragem
            FROM pedido
            WHERE id = %s AND deletado = FALSE
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (pedido_id,))
            row = cur.fetchone()

        if not row:
            return None

        return PedidoVO(
            pedido_id=row[0],
            cliente=row[1],
            con_email=row[2],
            con_telefone=row[3],
            tipo=row[4],
            outro=row[5],
            endereco=row[6],
            metragem=row[7],
            projetos=self.listar_arquivos_por_tipo(row[0], "projeto"),
            fotos=self.listar_arquivos_por_tipo(row[0], "foto")
        )

    # UPDATE
    def atualizar(self, pedido: PedidoVO) -> bool:
        sql = """
            UPDATE pedido
            SET nome_cliente = %s, 
                whatsapp = %s,
                email = %s,
                tipo = %s,
                outro = %s,
                endereco = %s,
                metragem = %s
            WHERE id = %s
              AND deletado = FALSE
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (
                pedido.get_cliente(),
                pedido.get_telefone(),
                pedido.get_email(),
                pedido.get_tipo(),
                pedido.get_outro(),
                pedido.get_endereco(),
                pedido.get_metragem(),
                pedido.get_id()
            ))
            atualizado = cur.rowcount > 0

        self._conn.commit()
        return atualizado

    # SOFT DELETE
    def deletar(self, pedido_id: int) -> bool:
        sql = """
            UPDATE pedido
            SET deletado = TRUE
            WHERE id = %s
              AND deletado = FALSE
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (pedido_id,))
            deletado = cur.rowcount > 0

        self._conn.commit()
        return deletado

    def add_arquivo(self, pedido_id: int, arquivo_uuid: str, tipo: str) -> None:
        sql = """
            INSERT INTO pedido_arquivo (pedido_id, arquivo_uuid, tipo)
            VALUES (%s, %s, %s)
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (
                pedido_id,
                arquivo_uuid,
                tipo
            ))

        self._conn.commit()

    def listar_arquivos_por_tipo(self, pedido_id: int, tipo: str) -> list[str]:
        sql = """
            SELECT arquivo_uuid
            FROM pedido_arquivo
            WHERE pedido_id = %s
              AND tipo = %s
        """

        with self._conn.cursor() as cur:
            cur.execute(sql, (pedido_id, tipo))
            rows = cur.fetchall()

        return [row[0] for row in rows]
