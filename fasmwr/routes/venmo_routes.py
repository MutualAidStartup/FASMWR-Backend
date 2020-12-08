from flask import (Blueprint, request, jsonify)
from flask_cors import cross_origin
from app import db, bcrypt
from models import User, Request
import re

venmo_routes = Blueprint('venmo_routes', __name__)


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