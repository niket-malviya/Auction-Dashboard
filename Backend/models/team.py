from app import db
import uuid

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_name = db.Column(db.String, nullable=False)
    owner_name = db.Column(db.String, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    remaining_amount = db.Column(db.Float, nullable=False)
    max_players = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String, nullable=True)  # Added image URL for team
    total_players = db.Column(db.Integer, default=0)  # ➕ This tracks current player count
    gold = db.Column(db.Integer, default=0)     # Optional: if tracking by category
    silver = db.Column(db.Integer, default=0)
    bronze = db.Column(db.Integer, default=0)

    # New column: Tournament foreign key
    tournament_id = db.Column(
        db.Uuid(as_uuid=True),
        db.ForeignKey('tournament.id', ondelete="CASCADE"),
        nullable=False
    )

    # Relationships
    team_players = db.relationship("TeamPlayer", backref="team", lazy=True)

    # Optional: Relationship to Tournament model
    tournament = db.relationship("Tournament", backref=db.backref("teams", lazy=True, cascade="all, delete"))
