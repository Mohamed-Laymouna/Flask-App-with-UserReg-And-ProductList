from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    items_count = fields.Int(required=True)


class UserSchema(PlainUserSchema):
    products = fields.List(fields.Nested(PlainProductSchema()), dump_only=True)


class ProductSchema(PlainProductSchema):
    user_id = fields.Int(required=True, load_only=True)
    owner = fields.Nested(PlainUserSchema(), dump_only=True)


class ProductUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    items_count = fields.Int(required=True)
    user_id = fields.Int(required=False)
