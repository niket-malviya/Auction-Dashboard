from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    mobile_number = fields.Str(required=True, validate=validate.Length(equal=10))
    password = fields.Str(required=True, load_only=True)
    type = fields.Str(required=True, validate=validate.OneOf(["admin", "user"]))
