from datetime import datetime

from src import db


class PedidoModel(db.Model):
    __tablename__ = 'pedido'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    camisa_id = db.Column(db.Integer, db.ForeignKey('camisa.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pendente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    usuario = db.relationship('UsuarioModel', backref='pedidos')
    camisa = db.relationship('Camisa', backref='pedidos')
