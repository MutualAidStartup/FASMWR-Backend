from flask import (Blueprint, request, jsonify)
from flask_cors import cross_origin
from app import db, bcrypt
from models import User, Request
from random import randint, choice
from string import ascii_uppercase
from venmo_api import Client, AuthenticationApi, ApiClient, random_device_id
import requests
import re
import json

venmo_routes = Blueprint('venmo_routes', __name__)
device_id = random_device_id()

""" About the process to getting the auth token:
        The params are sent over https so they should be secure in transit.  We should
        make it clear to the users that their information is not being saved and that
        their username and password is deleted after being processed for security 
        reasons.  Once we verify they are good logins with venmo, we can then receive 
        the auth token and return it to the client.  
        We have a choice here depending on the TTL of the token:
            1. If short (1 hour->1 day): Send it to client to hold
            2. If longer (1 day -> inf): Save it to the user in the db to be referenced
            whenever logged into again
        This adjustment should be relatively easy.  For now I think I will do opt 2 since
        it can cover both bases.  The only adjustment is that we need to return a message
        to the user when their token has expired.
"""

@venmo_routes.route('/verifyVenmoAcc', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def verify_venmo_acc():
    """ verify the provided username and password against venmo and see if they accept the u and p """
    username = request.args.get('username',None)
    password = request.args.get('password',None)
    token = request.args.get('token',None)
    userId = request.args.get('userId',None)
    
    user = User.query.filter_by(id=userId).first()
    if user is None:
        return "Could not find User by that id",404

    # Verify User
    resp = User.verify_reset_token(token)

    #check if resp is not a string
    if isinstance(resp, str):
        return "Token expired", 403
    
    # Verify user with venmo
    authn_api = AuthenticationApi(api_client=ApiClient(), device_id=device_id)
    r = authn_api.authenticate_using_username_password(username=username, password=password)
    print(r)
    # if we get an error, that means either entered the username and password wrong or we need 2 factor authentication
    if r.get('body').get('error'):
        otp_secret = r['headers'].get('venmo-otp-secret')
        if not otp_secret:
            raise AuthenticationFailedError("Failed to get the otp-secret for the 2-factor authentication process. "
                                            "(check your password)")
        authn_api.send_text_otp(otp_secret=otp_secret)
        return jsonify(two_factor='1',token=None, otp_secret=otp_secret),200
    else:
        access_token = r['body']['access_token']

    confirm("Successfully logged in. Note your token and device-id")
    print(f"access_token: {access_token}\n"
            f"device-id: {authn_api.__device_id}")

    user.venmo_token = access_token
    db.session.commit()

    return jsonify(two_factor=None,token=access_token, otp_secret=None),200
    
def request_two_factor(otp_secret):
    """
        Requests two factor authentication text to be sent
    """
    
    venmo_url = url+"oauth/access_token"
    body = {
        'via':"sms"
        }
    headers = {
        'device-id': deviceId,
        'venmo-otp-secret': otp_secret,
        'Content-Type': 'application/json'
    }
    
    r = requests.post(venmo_url,data=json.dumps(body),headers=headers)
    print(r)

@venmo_routes.route('/verifyVenmoCode', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def verify_venmo_code():
    authn_api = AuthenticationApi(api_client=ApiClient(), device_id=device_id)
    
    user_otp = request.args.get('code', None)
    otp_secret = request.args.get('otp_secret', None)
    token = request.args.get('token',None)
    userId = request.args.get('userId',None)
    
    user = User.query.filter_by(id=userId).first()
    if user is None:
        return "Could not find User by that id",404

    # Verify User
    resp = User.verify_reset_token(token)

    #check if resp is not a string
    if isinstance(resp, str):
        return "Token expired", 403
    
    print(user_otp)
    auth_token = authn_api.authenticate_using_otp(user_otp, otp_secret)
    user.venmo_token = auth_token
    db.session.commit()
    return jsonify(token=auth_token)

@venmo_routes.route('/venmoLogOut', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def venmo_log_out():
    
    access_token = request.args.get('code', None)
    token = request.args.get('token',None)
    userId = request.args.get('userId',None)
    
    user = User.query.filter_by(id=userId).first()
    if user is None:
        return "Could not find User by that id",404

    # Verify User
    resp = User.verify_reset_token(token)

    #check if resp is not a string
    if isinstance(resp, str):
        return "Token expired", 403

    venmo = Client(access_token=access_token)

    venmo.log_out(access_token)

    user.venmo_token = None
    db.session.commit()
    return "successful venmo unlink",200

@venmo_routes.route('/getVenmoProfile', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def venmo_user_info():
    print("GETTING VENMO PROFILE")
    auth_token = request.args.get('venmo_token',None)
    api_client = ApiClient(access_token=auth_token)
    profile = api_client.call_api(resource_path="/me", method='GET')
    return jsonify(venmo_balance=profile["body"]["data"]["balance"]),200
