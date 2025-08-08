import uuid
from app.extensions import db

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    flat_no = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    mobile_number = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=True)
    
    bowler_type = db.Column(db.String, nullable=False)
    
    batter_type = db.Column(db.String, nullable=False)
    
    category = db.Column(db.String, db.CheckConstraint(
        "category IN ('gold', 'silver', 'bronze')", name="players_category_check"))
    
    status = db.Column(db.String, db.CheckConstraint(
        "status IN ('sold', 'unsold')", name="players_status_check"), default='unsold', nullable=False)
    
    tournament_id = db.Column(db.Uuid(as_uuid=True), db.ForeignKey('tournament.id'), nullable=False)
