from flask_restful import Api
from flask import Blueprint
from flask_wtf.csrf import CSRFProtect
from backend.apis.login import UserLogin, SendCodeAPI

csrf = CSRFProtect()

bp = Blueprint('api', __name__, url_prefix='/r/v1')
api = Api(bp)

# login
api.add_resource(UserLogin, "/login")
api.add_resource(SendCodeAPI, "/sms")


def api_init_app(app):
    api.init_app(app)
    app.register_blueprint(bp)


def init_app(app):
    api_init_app(app)



