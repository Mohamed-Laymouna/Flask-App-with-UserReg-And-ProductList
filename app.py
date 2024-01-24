import os

from flask import Flask, jsonify
from flask_smorest import Api

from mail import mail

from db import db
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

from resources.user import blp as UserBlueprint
from resources.product import blp as ProductBlueprint
from resources.review import blp as ReviewBlueprint
from resources.cart import blp as CartBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config.from_pyfile('mail.cfg')

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['DEBUG'] = True

    mail.init_app(app)

    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "0000"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    with app.app_context():
        db.create_all()

    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ReviewBlueprint)
    api.register_blueprint(CartBlueprint)
    

    return app
