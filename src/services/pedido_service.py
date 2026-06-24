from src.models.pedido_model import PedidoModel
from src import db
from src.models.usuario_model import UsuarioModel
from src.models.camisa_model import Camisa
from sqlalchemy.exc import OperationalError


class PedidoService:
    @staticmethod
    def criar_pedido(usuario_id, camisa_id, quantidade, total, status='pendente'):
        try:
            usuario = UsuarioModel.query.get(usuario_id)
            camisa = Camisa.query.get(camisa_id)

            print("USUARIO:", usuario)
            print("CAMISA:", camisa)

            if not usuario:
                print("Usuário não encontrado")
                return False

            if not camisa:
                print("Camisa não encontrada")
                return False

            pedido = PedidoModel(
                usuario_id=usuario_id,
                camisa_id=camisa_id,
                quantidade=quantidade,
                total=total,
                status=status,
            )
            db.session.add(pedido)
            db.session.commit()
            return pedido
        except OperationalError:
            return None

    @staticmethod
    def listar_pedidos():
        try:
            return PedidoModel.query.all()
        except OperationalError:
            return None

    @staticmethod
    def obter_pedido_por_id(pedido_id):
        try:
            return PedidoModel.query.get(pedido_id)
        except OperationalError:
            return None

    @staticmethod
    def atualizar_pedido(pedido_id, dados):
        try:
            pedido = PedidoModel.query.get(pedido_id)
            if not pedido:
                return False

            if dados.get('quantidade') is not None:
                pedido.quantidade = dados['quantidade']
            if dados.get('total') is not None:
                pedido.total = dados['total']
            if dados.get('status'):
                pedido.status = dados['status']

            db.session.commit()
            return pedido
        except OperationalError:
            return None

    @staticmethod
    def deletar_pedido(pedido_id):
        try:
            pedido = PedidoModel.query.get(pedido_id)
            if pedido:
                db.session.delete(pedido)
                db.session.commit()
                return True
            return False
        except OperationalError:
            return None
