from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    products = db.relationship("ProductModel", back_populates="owner", lazy="dynamic")

    reviews = db.relationship("ReviewModel", back_populates="user", lazy="dynamic")
    
    
    cart = db.relationship('CartModel', backref='user', uselist=False, cascade='all, delete-orphan', lazy=False)


    
    

    
    