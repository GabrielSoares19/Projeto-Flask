from src.models import camisa_model
from src import db

class CamisaService:
    @staticmethod
    def criar_camisa(nome, tamanho, cor, preco, time):
        nova_camisa = camisa_model.Camisa(nome=nome, tamanho=tamanho, cor=cor, preco=preco, time=time)
        db.session.add(nova_camisa)
        db.session.commit()
        return nova_camisa

    @staticmethod
    def obter_camisas():
        return camisa_model.Camisa.query.all()

   

    @staticmethod
    def atualizar_camisa(camisa_id, nome=None, tamanho=None, cor=None, preco=None, time=None):
        camisa = camisa_model.Camisa.query.get(camisa_id)
        if camisa:
            if nome:
                camisa.nome = nome
            if tamanho:
                camisa.tamanho = tamanho
            if cor:
                camisa.cor = cor
            if preco is not None:
                camisa.preco = preco
            if time:
                camisa.time = time
            db.session.commit()
        return camisa

    @staticmethod
    def deletar_camisa(camisa_id):
        camisa = camisa_model.Camisa.query.get(camisa_id)
        if camisa:
            db.session.delete(camisa)
            db.session.commit()
            return True
        return False

    @staticmethod
    def obter_camisa_por_id(camisa_id):
        return camisa_model.Camisa.query.get(camisa_id)
