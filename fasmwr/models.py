from app import db
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash # hashing for security


class User(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    name = db.Column(db.String(), unique=False)
    location = db.Column(db.String(), unique=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_email(self, email):
        return self.email == email