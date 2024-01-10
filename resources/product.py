from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import ProductModel
from schemas import ProductSchema, ProductUpdateSchema

blp = Blueprint("Products", __name__, description="Operations on products")


@blp.route("/product")
class ItemList(MethodView):
    @jwt_required()
    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        """Create new item"""

        product = ProductModel(**product_data)
        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the product.")

        return product

    @jwt_required()
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        """get products list"""
        return ProductModel.query.all()


@blp.route("/product/<string:product_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        """get product by ID"""
        product = ProductModel.query.get_or_404(product_id)
        return product

    @jwt_required()
    def delete(self, product_id):
        """delete product by ID"""
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "product deleted."}

    @jwt_required()
    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductSchema)
    def put(self, product_data, product_id):
        """update product"""
        product = ProductModel.query.get_or_404(product_id)

        if product:
            product.price = product_data["price"]
            product.name = product_data["name"]
            product.count = product_data["count"]
        else:
            product = ProductModel(**product_data)

        db.session.add(product)
        db.session.commit()

        return product
