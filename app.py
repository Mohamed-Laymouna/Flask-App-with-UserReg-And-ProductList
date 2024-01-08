from flask import Flask
from flask_smorest import Api

from db import db


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stores.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
api = Api(app)


if __name__ == "__main__":
    app.run(debug=True)
