from marshmallow import Schema, fields

class TeamSchema(Schema):
    id = fields.UUID(dump_only=True)
    team_name = fields.String(required=True)
    owner_name = fields.String(required=True)
    total_amount = fields.Decimal(required=True)
    remaining_amount = fields.Decimal(required=True)
    max_players = fields.Integer(required=True)
    total_players = fields.Integer(dump_only=True)     # ➕ Current number of players
    gold = fields.Integer(dump_only=True)        # ➕ Optional, based on category
    silver = fields.Integer(dump_only=True)
    bronze = fields.Integer(dump_only=True)
    img_url = fields.String(allow_none=True) 
    tournament_id = fields.UUID(required=True)
