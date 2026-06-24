from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, jsonify, make_response
from src.schemas import pedido_schema
from src.services.pedido_service import PedidoService
from src import api


class PedidoList(Resource):
    def get(self):
        pedidos = PedidoService.listar_pedidos()
        if pedidos is None:
            return make_response(jsonify({'message': 'Serviço indisponível (DB).'}), 503)
        schema = pedido_schema.PedidoSchema(many=True)
        return make_response(jsonify(schema.dump(pedidos)), 200)

    def post(self):
        schema = pedido_schema.PedidoSchema()
        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        pedido = PedidoService.criar_pedido(
            usuario_id=dados['usuario_id'],
            camisa_id=dados['camisa_id'],
            quantidade=dados['quantidade'],
            total=dados['total'],
            status=dados.get('status', 'pendente')
        )

        if pedido is None:
            return make_response(jsonify({'message': 'Serviço indisponível (DB).'}), 503)
        if pedido is False:
            return make_response(jsonify({'message': 'Usuário ou camisa inválidos.'}), 400)

        return make_response(jsonify(schema.dump(pedido)), 201)


class PedidoResource(Resource):
    def get(self, pedido_id):
        pedido = PedidoService.obter_pedido_por_id(pedido_id)
        if pedido is None:
            return make_response(jsonify({'message': 'Serviço indisponível (DB).'}), 503)
        if not pedido:
            return make_response(jsonify({'message': 'Pedido não encontrado.'}), 404)
        schema = pedido_schema.PedidoSchema()
        return make_response(jsonify(schema.dump(pedido)), 200)

    def put(self, pedido_id):
        schema = pedido_schema.PedidoSchema()
        try:
            dados = schema.load(request.json, partial=True)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        pedido = PedidoService.atualizar_pedido(pedido_id, dados)
        if pedido is None:
            return make_response(jsonify({'message': 'Serviço indisponível (DB).'}), 503)
        if pedido is False:
            return make_response(jsonify({'message': 'Pedido não encontrado.'}), 404)
        return make_response(jsonify(schema.dump(pedido)), 200)

    def delete(self, pedido_id):
        resultado = PedidoService.deletar_pedido(pedido_id)
        if resultado is None:
            return make_response(jsonify({'message': 'Serviço indisponível (DB).'}), 503)
        if resultado:
            return make_response(jsonify({'message': 'Pedido deletado com sucesso.'}), 200)
        return make_response(jsonify({'message': 'Pedido não encontrado.'}), 404)


api.add_resource(PedidoList, '/pedidos')
api.add_resource(PedidoResource, '/pedidos/<int:pedido_id>')
