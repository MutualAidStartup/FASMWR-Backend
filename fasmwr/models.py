from app import db
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash # hashing for security


class User(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)