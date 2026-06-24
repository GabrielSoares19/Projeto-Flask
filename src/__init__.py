# configuracao das bibliotecas externas/dependecias
# instanciar aqui e configurar
# configurar a connection para apontar para o confiig object do flask
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api
from sqlalchemy.exc import OperationalError


app = Flask(__name__)
app.config.from_object('connection.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
api = Api(app)


@app.errorhandler(OperationalError)
def handle_db_error(error):
	return jsonify({'message': 'Database connection error'}), 503




# TODO : Apontar os modelos criados para a orm conseguir criar as tabelas

from .models.usuario_model import UsuarioModel
from .models.camisa_model import Camisa
from .models.pedido_model import PedidoModel
from .views import usuario_view
from .views import camisa_view
from .views import pedido_view