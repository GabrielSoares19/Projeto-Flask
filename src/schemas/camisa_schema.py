from src import ma
from marshmallow import fields


class CamisaSchema(ma.Schema):

    id = fields.Integer(dump_only=True)

    nome = fields.Str(required=True)
    tamanho = fields.Str(required=True)
    cor = fields.Str(required=True)
    preco = fields.Float(required=True)
    time = fields.Str(required=True)