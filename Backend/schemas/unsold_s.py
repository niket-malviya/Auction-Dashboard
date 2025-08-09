from marshmallow import Schema, fields

class UnsoldPlayerSchema(Schema):
    id = fields.UUID(dump_only=True)
    player_id = fields.UUID(required=True)
    tournament_id = fields.UUID(required=True)
