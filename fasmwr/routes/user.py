from flask import (Blueprint, request, jsonify)
from flask_cors import cross_origin
from app import db, bcrypt
from models import User
from random import randint 

users = Blueprint('users', __name__)

@users.route('/Register', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def register():
    """ Register a new Mutual Aid """
    
    password = request.args.get('password', None)
    print(password)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    email = request.args.get('email', None)

    uid = randint(100, 1000000000)
    while(User.query.filter_by(id=uid).first() is not None):
        uid = randint(100, 1000000000)

    user = User(id=uid, email=email,password_hash=hashed_password, name="Unnamed Mutual Aid")

    db.session.add(user)
    db.session.commit()
    token = user.get_reset_token()
    return jsonify(valid=True,token=token,id=user.id),200

@users.route('/Login', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def login():
    """ login to your Mutual Aid """
    
    email = request.args.get('email', None)
    password = request.args.get('password', None)

    user = User.query.filter_by(email=email).first()

    # if no user under that email is found, return false
    if user is None:
        print("user is none")
        return "Email was incorrect", 406
    
    if user and bcrypt.check_password_hash(user.password_hash,password):
        # send an encrypted version of the token
        token = user.get_reset_token()
        return jsonify(valid=True,token=token,id=user.id), 200
    else:
        print("email: " + email + " and password: " + password + " was incorrect.")
        return "password was incorrect", 406

@users.route('/editAccount', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def edit_account():
    """ Modify an accounts data """

    user_id = request.args.get('userId', None) 
    email = request.args.get('email', None)
    name = request.args.get('name', None)
    location = request.args.get('location', None)
    link = request.args.get('link', None)
    description = request.args.get('description', None)
    image = request.args.get('image', None)
    # Check auth token
    token = request.args.get('token', None)
    if token is None:
        return "No token provided", 406

    if user_id is None:
        return "No User_ID provided", 400

    resp = User.verify_reset_token(token)
    #check if resp is not a string
    if not isinstance(resp, str):
        user = User.query.get_or_404(user_id)

        if email is not None:
            user.email = email

        if name is not None:
            user.name = name

        if location is not None:
            user.location = location

        if link is not None:
            user.link = link

        if description is not None:
            user.description = description

        db.session.commit()

        return "Updated information", 200
    else:
        return "Bad Token", 406

@users.route('/getAccountData', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def view_data():
    """ view an accounts data """
    
    user_id = request.args.get('userId', None) 
    # Check auth token
    token = request.args.get('token', None)

    if token is None:
        return "No token provided", 406

    if user_id is None:
        return "No User_ID provided", 400

    resp = User.verify_reset_token(token)
    #check if resp is not a string
    if not isinstance(resp, str):
        user = User.query.get_or_404(user_id)

        return jsonify(name=user.name,email=user.email,description=user.description,location=user.location,link=user.link,image=user.image), 200
    else:
        return "Token not valid", 400

@users.route('/getCardInfo', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def get_card_data():
    """ view an accounts data """

    user_id = request.args.get('id', None)
    max_num_cards = int(request.args.get('num_cards', None))
    count = 0
    cards = []

    if user_id is None:
        users = User.query.all()
        for user in users:
            if(count>=max_num_cards):
                break
            cards.append({
                "id":user.id,
                "name":user.name,
                "description":user.description,
                "link":user.link,
                "logo":user.image
            })
            count+=1
    else:
        user = User.query.filter_by(id=user_id).first()
        cards.append({
            "id":user.id,
            "name":user.name,
            "description":user.description,
            "link":user.link,
            "logo":user.image
        })

    

    
    return jsonify(cards=cards), 200
