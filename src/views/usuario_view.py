from flask_restful import Resource
from marshmallow import ValidationError
from src.schemas import usuario_schema
from flask import request, jsonify, make_response
from src.services import usuario_service
from src import api


class UsuarioList(Resource):

    def get(self):
        """
        Lista todos os usuários
        ---
        tags:
          - Usuários
        produces:
          - application/json
        responses:
          200:
            description: Lista de usuários
        """
        usuarios = usuario_service.listar_usuario()
        schema = usuario_schema.UsuarioSchema(many=True)
        return make_response(jsonify(schema.dump(usuarios)), 200)

    def post(self):
        """
        Cadastra um novo usuário
        ---
        tags:
          - Usuários
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  example: Gabriel
                email:
                  type: string
                  example: gabriel@email.com
                senha:
                  type: string
                  example: 123456
        responses:
          201:
            description: Usuário criado com sucesso
          400:
            description: Erro na requisição
        """
        schema = usuario_schema.UsuarioSchema()

        try:
            dados = schema.load(request.json)

        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        if usuario_service.listar_usuario_email(dados['email']):
            return make_response(
                jsonify({'message': 'E-mail já cadastrado.'}),
                400
            )

        try:
            resultado = usuario_service.cadastrar_usuario(dados)

            return make_response(
                jsonify(schema.dump(resultado)),
                201
            )

        except Exception as e:
            return make_response(
                jsonify({'message': str(e)}),
                400
            )


api.add_resource(UsuarioList, '/usuarios')


class UsuarioResource(Resource):

    def get(self, id_usuario):
        """
        Busca um usuário pelo ID
        ---
        tags:
          - Usuários
        parameters:
          - name: id_usuario
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Usuário encontrado
          404:
            description: Usuário não encontrado
        """
        usuario = usuario_service.listar_usuario_id(id_usuario)

        if usuario:
            schema = usuario_schema.UsuarioSchema()

            return make_response(
                jsonify(schema.dump(usuario)),
                200
            )

        return make_response(
            jsonify({'message': 'Usuario não encontrado.'}),
            404
        )

    def put(self, id_usuario):
        """
        Atualiza um usuário
        ---
        tags:
          - Usuários
        parameters:
          - name: id_usuario
            in: path
            type: integer
            required: true
          - in: body
            name: body
            schema:
              type: object
        responses:
          200:
            description: Usuário atualizado
          404:
            description: Usuário não encontrado
        """
        schema = usuario_schema.UsuarioSchema()

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

        usuario = usuario_service.editar_usuario(
            id_usuario,
            dados
        )

        if usuario:
            return make_response(
                jsonify(schema.dump(usuario)),
                200
            )

        return make_response(
            jsonify({'message': 'Usuario não encontrado.'}),
            404
        )

    def delete(self, id_usuario):
        """
        Remove um usuário
        ---
        tags:
          - Usuários
        parameters:
          - name: id_usuario
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Usuário removido
          404:
            description: Usuário não encontrado
        """
        if usuario_service.deletar_usuario(id_usuario):
            return make_response(
                jsonify({'message': 'Usuário deletado com sucesso!'}),
                200
            )

        return make_response(
            jsonify({'message': 'Usuário não encontrado!'}),
            400


        )


api.add_resource(
    UsuarioResource,
    '/usuarios/<int:id_usuario>'
)