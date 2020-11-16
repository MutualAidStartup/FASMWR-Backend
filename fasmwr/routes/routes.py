from flask import Blueprint

fasmwr = Blueprint('fasmwr', __name__)

@fasmwr.route('/time')
def get_current_time():
    return {'time': time.time()}