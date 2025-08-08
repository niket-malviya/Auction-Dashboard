from marshmallow import Schema, fields

class SportTypeSchema(Schema):
    id = fields.UUID(dump_only=True)
    sport_name = fields.String(required=True)
