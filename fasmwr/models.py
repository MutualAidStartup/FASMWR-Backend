from app import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash # hashing for security


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    name = db.Column(db.String(), unique=False)
    location = db.Column(db.String(), unique=False)
    description = db.Column(db.String(), unique=False)
    link = db.Column(db.String(), unique=False)
    image = db.Column(db.String(), unique=False)

    requests = db.relationship('Request', backref='user', cascade="all, delete, delete-orphan")

    def get_reset_token(self, expires_sec=3600):
        """
        Generates the Auth Token
        :return: string
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return User.query.get(id)

class Request(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    situation = db.Column(db.String)
    identities = db.Column(db.String)
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)