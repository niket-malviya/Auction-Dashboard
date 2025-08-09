import uuid
from app.extensions import db

class TeamPlayer(db.Model):
    __tablename__ = 'team_players'

    team_id = db.Column(db.Uuid(as_uuid=True), db.ForeignKey('teams.id'), primary_key=True, default=uuid.uuid4)
    player_id = db.Column(db.Uuid(as_uuid=True), db.ForeignKey('players.id'), primary_key=True, nullable=False)
    tournament_id = db.Column(db.Uuid(as_uuid=True), db.ForeignKey('tournament.id'), primary_key=True, nullable=False)
    bid_amount = db.Column(db.Float, nullable=False)
