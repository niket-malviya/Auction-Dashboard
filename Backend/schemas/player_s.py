from marshmallow import Schema, fields, validate

class PlayerSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    last_name = fields.String(required=True)
    flat_no = fields.String(required=True)
    age = fields.Integer(required=True, validate=validate.Range(min=1, max=100))
    mobile_number = fields.String(required=True, validate=validate.Length(equal=10))
    img_url = fields.String(allow_none=True)
    bowler_type = fields.String(required=True)
    batter_type = fields.String(required=True)
    category = fields.String(required=True, validate=validate.OneOf(['gold', 'silver', 'bronze']))
    status = fields.String(validate=validate.OneOf(['sold', 'unsold','available']))
    tournament_id = fields.UUID(required=True)
