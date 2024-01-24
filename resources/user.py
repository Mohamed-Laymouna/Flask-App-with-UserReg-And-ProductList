from models import UserModel
from passlib.hash import pbkdf2_sha256  # hashing password
from flask import url_for
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import UserSchema, UserEmailVerificationSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from db import db

from blocklist import BLOCKLIST
from flask_mail import Message
from mail import mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

blp = Blueprint('Users', 'users', description='Operations on users')

serializer = URLSafeTimedSerializer("0000")


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

        token = serializer.dumps(user.email, salt="email-confirm")
        msg = Message('Confirm Email',
                      sender='intelligent.hometechnology@gmail.com',
                      recipients=[user.email])

        link = url_for('Users.UserEmailVerification', token=token, _external=True)
        msg.body = 'Please click the following link to verify your account {}'.format(link)

        mail.send(msg)

        return {"message": "User created successfully. Please check your email to verify your Email"}, 200


@blp.route('/confirm_email/<token>')
class UserEmailVerification(MethodView):
    @blp.response(200)
    def get(self, token):
        """Verify user email"""
        try:
            email = serializer.loads(token, salt='email-confirm', max_age=3600)
        except SignatureExpired:
            return 'The token is expired!'

        user = UserModel.query.filter(UserModel.email == email).first()
        user.is_verified = True
        db.session.commit()
        # return '<h1>The token works for {}</h1>'.format(user.email)
        # return 'Account activated! your E-mail {} is now verified.'.format(user.email), 200
        return {"message": "Email verified successfully"}, 200


@blp.route("/resend")
class UserResendConfirmation(MethodView):
    @blp.arguments(UserEmailVerificationSchema)
    @blp.response(200)
    def get(self, user_data):
        """Resend verification email"""
        user = UserModel.query.filter(UserModel.email == user_data["email"]).first()
        if not user:
            abort(401, message="Invalid credentials.")
        if user.is_verified:
            abort(400, message="Account already verified.")
        token = serializer.dumps(user.email, salt="email-confirm")
        msg = Message('Confirm Email',
                      sender='intelligent.hometechnology@gmail.com',
                      recipients=[user.email])

        link = url_for('Users.UserEmailVerification', token=token, _external=True)
        msg.body = 'Please click the following link to verify your account {}'.format(link)

        mail.send(msg)

        return {
            "message": "verification has been resent successfully. Please check your email to verify your account"}, 200


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """User login"""
        user = UserModel.query.filter(UserModel.email == user_data["email"]).first()
        if not user.is_verified:
            abort(401, message="Email is not verified. Please verify your email")

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)

            return {'message': 'user login successfully', "access_token": access_token}, 200

        abort(401, message="Invalid credentials.")


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
            return {"message": "User deleted Successfully"}
        else:
            return {"message": "User not found"}


@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self):
        """User logout"""
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200