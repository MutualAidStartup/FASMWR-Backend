from flask import (Blueprint, request, jsonify)
from flask_cors import cross_origin
from app import db

fasmwr = Blueprint('fasmwr', __name__)

@fasmwr.route('/')
def test():
    return "This is a test!"

@fasmwr.route('/time')
def get_current_time():
    return {'time': time.time()}

@fasmwr.route('/requestAid', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def submit_aid_request():
    situation = request.args.get('situation', None)
    if situation is None:
        return "No situation given", 404
    identity = request.args.get('identity', None)
    if situation is None:
        return "No identity given", 404
    requestedAmount = request.args.get('requestedAmount', None)
    if situation is None:
        return "No requestedAmount given", 404

    print("The info is as follows: " + situation + " " + identity + " " + requestedAmount)

    print("Submitting aid request!")
    return "Success", 200