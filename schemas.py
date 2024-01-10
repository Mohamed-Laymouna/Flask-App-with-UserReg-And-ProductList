from marshmallow import Schema, fields, validate


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    count = fields.Int(required=True)


class PlainReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    rating = fields.Float(required=True, validate=validate.Range(min=1, max=5))
    review = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)


class UserSchema(PlainUserSchema):
    products = fields.List(fields.Nested(PlainProductSchema()), dump_only=True)
    reviews = fields.List(fields.Nested(PlainReviewSchema()), dump_only=True)


class ProductSchema(PlainProductSchema):
    user_id = fields.Int(required=True, load_only=True)
    owner = fields.Nested(PlainUserSchema(), dump_only=True)
    reviews = fields.List(fields.Nested(PlainReviewSchema()), dump_only=True)


class ProductUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    count = fields.Int(required=False)
    user_id = fields.Int(required=True)


class ReviewSchema(PlainReviewSchema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)

    product_id = fields.Int(required=False, load_only=True)
    product = fields.Nested(PlainProductSchema(), dump_only=True)
