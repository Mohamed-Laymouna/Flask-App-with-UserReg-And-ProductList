from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import ReviewModel, ProductModel
from schemas import ReviewSchema

blp = Blueprint("Reviews", __name__, description="Operations on Reviews")


@blp.route('/<int:product_id>/reviews')
class ReviewById(MethodView):
    @blp.response(200, ReviewSchema(many=True))
    def get(self, product_id):
        """List reviews for a product"""
        reviews = ReviewModel.query.filter_by(product_id=product_id).all()
        return reviews

    @jwt_required()
    @blp.arguments(ReviewSchema)
    @blp.response(201, ReviewSchema)
    def post(self, new_review, product_id):
        """Create a new review for a product"""
        product = ProductModel.query.get_or_404(product_id)
        if new_review['user_id'] == product.user_id:
            abort(403, message="The owner cannot review their own product.")

        new_review["product_id"] = product_id
        review = ReviewModel(**new_review)
        db.session.add(review)
        db.session.commit()
        return review


@blp.route('/reviews/<int:review_id>')
class ReviewById(MethodView):
    @jwt_required()
    def delete(self, review_id):
        """Delete a review by ID"""
        review = ReviewModel.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return {"message": "review deleted."}


