import uuid
from app.extensions import db

class SportType(db.Model):
    __tablename__ = 'sport_type'

    id = db.Column(db.Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sport_name = db.Column(db.String, nullable=False)
