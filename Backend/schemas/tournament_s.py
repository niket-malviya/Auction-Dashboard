from marshmallow import Schema, fields, validate

class TournamentSchema(Schema):
    id = fields.UUID(dump_only=True)
    users_id = fields.UUID(required=True)
    name = fields.Str(required=True)
    sport_id = fields.UUID(required=True)
    tournament_type = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    venue = fields.Str(required=True)
