import uuid
from app.extensions import db

class UnsoldPlayer(db.Model):
    __tablename__ = 'unsold_players'

    id = db.Column(db.Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = db.Column(db.Uuid(as_uuid=True), db.ForeignKey('players.id'), nullable=False)
    tournament_id = db.Column(db.Uuid(as_uuid=True), db.ForeignKey('tournament.id'), nullable=False)
