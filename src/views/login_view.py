from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from src import api
from src.services import usuario_service


class Login(Resource):
    def post(self):
        """
        Login do usuário
        ---
        tags:
          - Autenticação
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - email
                - senha
              properties:
                email:
                  type: string
                  example: gabriel@email.com
                senha:
                  type: string
                  example: 123456
        responses:
          200:
            description: Login realizado com sucesso
            schema:
              type: object
              properties:
                access_token:
                  type: string
                usuario:
                  type: string
          401:
            description: Senha inválida
          404:
            description: Usuário não encontrado
        """

        dados = request.get_json()

        email = dados.get("email")
        senha = dados.get("senha")

        usuario = usuario_service.listar_usuario_email(email)

        if not usuario:
            return make_response(jsonify({
                "message": "Usuário não encontrado."
            }), 404)

        if not usuario.verifica_senha(senha):
            return make_response(jsonify({
                "message": "Senha inválida."
            }), 401)

        token = create_access_token(identity=str(usuario.id))

        return make_response(jsonify({
            "access_token": token,
            "usuario": usuario.nome
        }), 200)


api.add_resource(Login, "/login")