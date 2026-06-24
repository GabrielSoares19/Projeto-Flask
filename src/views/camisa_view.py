from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, jsonify, make_response
from src.services.camisa_service import CamisaService
from src.schemas.camisa_schema import CamisaSchema
from src import api

class CamisaList(Resource):
    def get(self):
        camisas = CamisaService.obter_camisas()
        schema = CamisaSchema(many=True)
        return make_response(jsonify(schema.dump(camisas)), 200)
    def post(self):
        schema = CamisaSchema()

        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            nova_camisa = CamisaService.criar_camisa(**dados)
            return make_response(jsonify(schema.dump(nova_camisa)), 201)
        
        except Exception as e:
            return make_response(jsonify({'message':str(e)}), 400)
api.add_resource(CamisaList, '/camisas')

class CamisaResource(Resource):
    def get(self, id_camisa):
        camisa = CamisaService.obter_camisa_por_id(id_camisa)
        if camisa:
            schema = CamisaSchema()
            return make_response(jsonify(schema.dump(camisa)), 200)
        return make_response(jsonify({'message':"Camisa não encontrada."}), 404)
    def put(self, id_camisa):
        schema = CamisaSchema()

        try:
            dados = schema.load(request.json, partial=True)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        camisa_atualizada = CamisaService.atualizar_camisa(id_camisa, **dados)
        if camisa_atualizada:
            return make_response(jsonify(schema.dump(camisa_atualizada)), 200)
        return make_response(jsonify({'message':"Camisa não encontrada."}), 404)
    def delete(self, id_camisa):
        sucesso = CamisaService.deletar_camisa(id_camisa)
        if sucesso:
            return make_response(jsonify({'message':"Camisa deletada com sucesso."}), 200)
        return make_response(jsonify({'message':"Camisa não encontrada."}), 404)
api.add_resource(CamisaResource, '/camisas/<int:id_camisa>')


