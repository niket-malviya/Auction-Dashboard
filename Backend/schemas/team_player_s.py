from marshmallow import Schema, fields

class TeamPlayerSchema(Schema):
    team_id = fields.UUID(required=True)
    player_id = fields.UUID(required=True)
    tournament_id = fields.UUID(required=True)
    bid_amount = fields.Float(required=True)
    
