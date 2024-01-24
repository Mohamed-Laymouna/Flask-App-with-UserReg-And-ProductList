from db import db


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    owner = db.relationship("UserModel", back_populates="products")

    reviews = db.relationship("ReviewModel", back_populates="product", lazy="dynamic")
    
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), unique=False, nullable=True)
    
    cart_items = db.relationship('CartItemModel', backref='product', lazy=True, cascade='all, delete-orphan')

    
    
    
    
    