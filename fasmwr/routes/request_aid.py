from flask import (Blueprint, request, jsonify)
from flask_cors import cross_origin
from app import db, bcrypt
from models import User, Request
import re

requestAid = Blueprint('requestAid', __name__)

@requestAid.route('/requestAid', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def request_from():
    """ request money from a new Mutual Aid """
    
    user_id = request.args.get('user_id', None)
    situation = request.args.get('situation', None)
    identities = request.args.get('identities', None)
    amount = request.args.get('amount', None)
    
    #Keeping this here as a note to how to get the elements of the identity
    #identities_array = re.split(', |,',identities)

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return "Could not find a mutual aid by that id", 404

    request_obj = Request(situation=situation,identities=identities,amount=amount, user_id=user_id)

    db.session.add(request_obj)
    db.session.commit()

    #return the id so the requestor can search up their 'ticket' and know their progress
    return jsonify(id=request_obj.id),200

@requestAid.route('/view_requests', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def get_request_list():
    """ view requests for a new Mutual Aid 
        -NOTE- This does not require a token.  This is because we want to be completely transparent
        and so this function will later be able to be used by the public to view a mutual aids impact
    """

    request_list = []
    
    user_id = request.args.get('user_id', None)
    num_requests = int(request.args.get('num_requests', None))

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return "Could not find a Mutual Aid by that id",404

    requests = Request.query.filter_by(user_id=user_id).all()

    if num_requests <= 0:
        for request_item in requests:
            request_list.append({
                "id":request_item.id,
                "identity":request_item.identity,
                "situation":request_item.situation,
                "amount":request_item.amount,
            })
    else:
        counter = 0
        for request_item in requests:
            if counter == num_requests:
                break
            request_list.append({
                "id":request_item.id,
                "identities":request_item.identities,
                "situation":request_item.situation,
                "amount":request_item.amount,
            })

    return jsonify(request=request_list),200
    
@requestAid.route('/removeRequest', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def remove_request():
    """ Remove a request from the database """
    
    user_id = request.args.get('userId', None)
    token = request.args.get('token', None)
    request_id = request.args.get('request_id', None)
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return "Could not find User by that id",404

    # Verify User
    resp = User.verify_reset_token(token)

    #check if resp is not a string
    if isinstance(resp, str):
        return "Token expired", 403
    
    request_obj = Request.query.filter_by(id=request_id).first()

    if request_obj is not None:
        print("found a request")

        db.session.flush()

        db.session.delete(request_obj)

        db.session.commit()

    return "Removed", 200