from flask import Flask
from flask_restful import Api
from flask_sockets import Sockets

api = Api(prefix="/api")

_app = Flask(__name__)
sockets = Sockets(_app)
from application import websockets

def create_app():
    _app.config.from_object("config.Config")

    api.init_app(_app)

    with _app.app_context():
        from application import routes
        return _app
