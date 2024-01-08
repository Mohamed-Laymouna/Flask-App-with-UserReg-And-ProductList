from models import UserModel
from passlib.hash import pbkdf2_sha256  # hashing password
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import UserSchema
from db import db

blp = Blueprint('Users', 'users', description='Operations on users')


@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Register a new user"""

        if UserModel.query.filter(UserModel.username == user_data['username']).first():
            abort(400, message="User already exists")

        user = UserModel(username=user_data['username'],
                         phone=user_data['phone'],
                         email=user_data['email'],
                         password=pbkdf2_sha256.hash(user_data['password']))
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully."}, 200


@blp.route('/users')
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """get all users"""

        return UserModel.query.all()


@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """get user by id"""

        user = UserModel.query.get(user_id)
        if user:
            return user
        else:
            abort(404, message="User not found")

    def delete(self, user_id):
        """Delete user by id"""

        user = UserModel.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"}
        else:
            return {"message": "User not found"}