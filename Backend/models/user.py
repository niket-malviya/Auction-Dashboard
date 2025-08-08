import uuid
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # e.g. "admin", "user"

    def __repr__(self):
        return f"<User {self.name}>"
