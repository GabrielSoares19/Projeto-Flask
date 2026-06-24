from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from src.schemas import pedido_schema
from src.services.pedido_service import PedidoService
from src import api


class PedidoList(Resource):

    @jwt_required()
    def get(self):
        """
        Lista todos os pedidos
        ---
        tags:
          - Pedidos
        security:
          - Bearer: []
        produces:
          - application/json
        responses:
          200:
            description: Lista de pedidos
          401:
            description: Não autorizado
        """

        pedidos = PedidoService.listar_pedidos()

        if pedidos is None:
            return make_response(
                jsonify({'message': 'Serviço indisponível (DB).'}),
                503
            )

        schema = pedido_schema.PedidoSchema(many=True)

        return make_response(
            jsonify(schema.dump(pedidos)),
            200
        )


    @jwt_required()
    def post(self):
        """
        Cadastra um novo pedido
        ---
        tags:
          - Pedidos
        security:
          - Bearer: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                usuario_id:
                  type: integer
                  example: 1
                camisa_id:
                  type: integer
                  example: 1
                quantidade:
                  type: integer
                  example: 2
                total:
                  type: number
                  example: 599.80
                status:
                  type: string
                  example: pendente
        responses:
          201:
            description: Pedido criado com sucesso
          400:
            description: Erro ao criar pedido
          401:
            description: Não autorizado
        """

        schema = pedido_schema.PedidoSchema()

        try:
            dados = schema.load(request.json)

        except ValidationError as err:
            return make_response(
                jsonify(err.messages),
                400
            )

        pedido = PedidoService.criar_pedido(
            usuario_id=dados['usuario_id'],
            camisa_id=dados['camisa_id'],
            quantidade=dados['quantidade'],
            total=dados['total'],
            status=dados.get('status', 'pendente')
        )

        if pedido is None:
            return make_response(
                jsonify({'message': 'Erro ao criar pedido.'}),
                400
            )

        return make_response(
            jsonify(schema.dump(pedido)),
            201
        )


class PedidoResource(Resource):

    @jwt_required()
    def get(self, pedido_id):
        """
        Busca um pedido pelo ID
        ---
        tags:
          - Pedidos
        security:
          - Bearer: []
        parameters:
          - name: pedido_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Pedido encontrado
          404:
            description: Pedido não encontrado
          401:
            description: Não autorizado
        """

        pedido = PedidoService.obter_pedido_por_id(pedido_id)

        if pedido is None:
            return make_response(
                jsonify({'message': 'Pedido não encontrado.'}),
                404
            )

        schema = pedido_schema.PedidoSchema()

        return make_response(
            jsonify(schema.dump(pedido)),
            200
        )


    @jwt_required()
    def put(self, pedido_id):
        """
        Atualiza um pedido
        ---
        tags:
          - Pedidos
        security:
          - Bearer: []
        parameters:
          - name: pedido_id
            in: path
            type: integer
            required: true
          - in: body
            name: body
            schema:
              type: object
        responses:
          200:
            description: Pedido atualizado
          404:
            description: Pedido não encontrado
          401:
            description: Não autorizado
        """

        schema = pedido_schema.PedidoSchema()

        try:
            dados = schema.load(
                request.json,
                partial=True
            )

        except ValidationError as err:
            return make_response(
                jsonify(err.messages),
                400
            )

        pedido = PedidoService.atualizar_pedido(
            pedido_id,
            dados
        )

        if pedido is None:
            return make_response(
                jsonify({'message': 'Erro ao atualizar pedido.'}),
                400
            )

        if pedido is False:
            return make_response(
                jsonify({'message': 'Pedido não encontrado.'}),
                404
            )

        return make_response(
            jsonify(schema.dump(pedido)),
            200
        )


    @jwt_required()
    def delete(self, pedido_id):
        """
        Remove um pedido
        ---
        tags:
          - Pedidos
        security:
          - Bearer: []
        parameters:
          - name: pedido_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Pedido removido com sucesso
          404:
            description: Pedido não encontrado
          401:
            description: Não autorizado
        """

        resultado = PedidoService.deletar_pedido(
            pedido_id
        )

        if resultado:
            return make_response(
                jsonify({'message': 'Pedido deletado com sucesso.'}),
                200
            )

        return make_response(
            jsonify({'message': 'Pedido não encontrado.'}),
            404
        )


api.add_resource(PedidoList, '/pedidos')
api.add_resource(PedidoResource, '/pedidos/<int:pedido_id>')