from src import db


class Camisa(db.Model):
    __tablename__ = 'camisa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tamanho = db.Column(db.String(10), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    time = db.Column(db.String(100), nullable=False)

  