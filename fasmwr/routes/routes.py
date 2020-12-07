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