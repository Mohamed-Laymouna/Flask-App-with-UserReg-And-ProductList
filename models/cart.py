from db import db
#from datetime import datetime


class CartModel(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_cost = db.Column(db.Float, nullable=False, default=0.0) #db.Numeric(precision=100, scale=2)
    total_cost_with_vat = db.Column(db.Numeric(precision=100, scale=2), nullable=False, default=0.0)
    items = db.relationship('CartItemModel', backref='cart', lazy=True, cascade='all, delete-orphan')



class CartItemModel(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), unique=False, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), unique=False, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False)

    #product = db.relationship('ProductModel', backref='cart_items')










