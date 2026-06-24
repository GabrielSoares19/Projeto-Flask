from src.models.pedido_model import PedidoModel
from src import db
from sqlalchemy.exc import OperationalError


class PedidoService:

    @staticmethod
    def criar_pedido(usuario_id, camisa_id, quantidade, total, status='pendente'):
        try:
            pedido = PedidoModel(
                usuario_id=usuario_id,
                camisa_id=camisa_id,
                quantidade=quantidade,
                total=total,
                status=status
            )

            db.session.add(pedido)
            db.session.commit()

            return pedido

        except Exception as e:
            db.session.rollback()
            print("ERRO AO CRIAR PEDIDO:", e)
            return None

    @staticmethod
    def listar_pedidos():
        try:
            return PedidoModel.query.all()

        except Exception as e:
            print("ERRO AO LISTAR PEDIDOS:", e)
            return None

    @staticmethod
    def obter_pedido_por_id(pedido_id):
        try:
            return PedidoModel.query.get(pedido_id)

        except Exception as e:
            print("ERRO AO BUSCAR PEDIDO:", e)
            return None

    @staticmethod
    def atualizar_pedido(pedido_id, dados):
        try:
            pedido = PedidoModel.query.get(pedido_id)

            if not pedido:
                return False

            if "usuario_id" in dados:
                pedido.usuario_id = dados["usuario_id"]

            if "camisa_id" in dados:
                pedido.camisa_id = dados["camisa_id"]

            if "quantidade" in dados:
                pedido.quantidade = dados["quantidade"]

            if "total" in dados:
                pedido.total = dados["total"]

            if "status" in dados:
                pedido.status = dados["status"]

            db.session.commit()

            return pedido

        except Exception as e:
            db.session.rollback()
            print("ERRO AO ATUALIZAR PEDIDO:", e)
            return None

    @staticmethod
    def deletar_pedido(pedido_id):
        try:
            pedido = PedidoModel.query.get(pedido_id)

            if not pedido:
                return False

            db.session.delete(pedido)
            db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()
            print("ERRO AO DELETAR PEDIDO:", e)
            return None