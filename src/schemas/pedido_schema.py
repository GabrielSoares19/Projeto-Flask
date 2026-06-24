from src import ma
from src.models import pedido_model
from marshmallow import fields


class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = pedido_model.PedidoModel
        fields = ('id', 'usuario_id', 'camisa_id', 'quantidade', 'total', 'status', 'created_at')

    usuario_id = fields.Int(required=True)
    camisa_id = fields.Int(required=True)
    quantidade = fields.Int(required=True)
    total = fields.Float(required=True)
    status = fields.Str(required=False, load_default='pendente')
