from db import db
from datetime import datetime


class ReviewModel(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    user = db.relationship("UserModel", back_populates="reviews")

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), unique=False, nullable=False)
    product = db.relationship("ProductModel", back_populates="reviews")