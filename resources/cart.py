from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import CartModel, ProductModel, CartItemModel
from schemas import CartSchema, CartItemSchema

blp = Blueprint("cart", __name__, description="Operations on cart")


@blp.route("/cart/<int:user_id>")
class Cart(MethodView):
    @blp.arguments(CartItemSchema)
    @blp.response(200, CartSchema)
    def post(self, data, user_id):
        """add new item to cart"""
        cart = CartModel.query.filter_by(user_id=user_id).first()
        product = ProductModel.query.filter_by(id=data['product_id']).first()

        if product.stock < data['quantity']:
            abort(400, message="Not enough stock")

        if not cart:
            cart = CartModel(user_id=user_id)
            db.session.add(cart)
            db.session.commit()

        cart_item = CartItemModel.query.filter_by(cart_id=cart.id, product_id=product.id).first()

        if not cart_item:

            cart_item = CartItemModel(cart_id=cart.id, product_id=product.id, name=product.name,
                                      quantity=data['quantity'], price=product.price)

            db.session.add(cart_item)
            # db.session.commit()

        else:
            cart_item.quantity += data['quantity']

        cart.total_cost = sum(cart_item.price * cart_item.quantity for cart_item in cart.items)
        cart.total_cost_with_vat = cart.total_cost * 1.14
        db.session.commit()

        return cart, 201

    @blp.response(200, CartSchema)
    def get(self, user_id):
        """get cart by user id"""
        cart = CartModel.query.filter_by(user_id=user_id).first()
        if not cart:
            abort(404, message="Cart not found")
        return cart, 200

    # update quantity of item in cart
    @blp.arguments(CartItemSchema)
    @blp.response(200, CartSchema)
    def put(self, data, user_id):
        """update quantity of item in cart"""
        cart = CartModel.query.filter_by(user_id=user_id).first()
        product = ProductModel.query.filter_by(id=data['product_id']).first()

        if product.stock < data['quantity']:
            abort(400, message="Not enough stock")

        cart_item = CartItemModel.query.filter_by(cart_id=cart.id, product_id=product.id).first()

        if not cart_item:
            abort(404, message="Item not found")

        cart_item.quantity = data['quantity']

        cart.total_cost = sum(cart_item.price * cart_item.quantity for cart_item in cart.items)
        cart.total_cost_with_vat = cart.total_cost * 1.14
        db.session.commit()

        return cart, 200


# remove item from cart
@blp.route("/cart/<int:user_id>/<int:product_id>")
class CartItem(MethodView):
    @blp.response(200, CartSchema)
    def delete(self, user_id, product_id):
        """delete item from cart"""
        cart = CartModel.query.filter_by(user_id=user_id).first()
        product = ProductModel.query.filter_by(id=product_id).first()
        cart_item = CartItemModel.query.filter_by(cart_id=cart.id, product_id=product.id).first()

        if not cart_item:
            abort(404, message="Item not found")

        db.session.delete(cart_item)

        cart.total_cost = sum(cart_item.price * cart_item.quantity for cart_item in cart.items)
        cart.total_cost_with_vat = cart.total_cost * 1.14

        db.session.commit()

        return cart, 202
