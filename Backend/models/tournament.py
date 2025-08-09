from app import db
import uuid
from datetime import date

class Tournament(db.Model):
    __tablename__ = 'tournament'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    users_id = db.Column(db.Uuid, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sport_id = db.Column(db.Uuid, db.ForeignKey('sport_type.id'), nullable=False)
    tournament_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    venue = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<Tournament {self.name}>"
