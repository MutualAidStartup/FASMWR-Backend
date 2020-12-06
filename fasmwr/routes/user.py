from flask import (Blueprint, request, jsonify)
from flask_cors import cross_origin
from app import db, bcrypt
from models import User

users = Blueprint('users', __name__)

@users.route('/requestAid', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def register():
    """ Register a new Mutual Aid """
    
    hashed_password = bcrypt.generate_password_hash(request.args.get('password', None))
    email = request.args.get('email', None)

    user = User(email=email,password=hashed_password, name="Unnamed Mutual Aid")

    db.session.add(user)
    db.session.commit()
    return "Successfully created a Mutal Aid!",200

@users.route('/login', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def login():
    """ login to your Mutual Aid """
    
    password = request.args.get('password', None)
    email = request.args.get('email', None)

    user = User.query.filter_by(email=email).first()

    # if no user under that email is found, return false
    if user is None:
        return jsonify(valid=False,token=None)
    
    if user.check_email(email) && user.check_password(password):
        # send an encrypted version of the token
        token = bcrypt.generate_password_hash(user.token)
        return jsonify(valid=True,token=token), 200
    else
        return jsonify(valid=False,token=None), 406

@users.route('/editAccount', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def edit_account():
    """ Modify an accounts data """

    user_id = request.args.get('userId', None) 
    email = request.args.get('email', None)
    name = request.args.get('name', None)
    location = request.args.get('location', None)

    if user_id is None:
        return "No User_ID provided", 400

    user = User.query.get_or_404(user_id)

    if email is not None:
        user.email = email

    if name is not None:
        user.name = name

    if location is not None:
        user.location = location

    return "Updated information", 200
