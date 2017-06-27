from flask import Blueprint
import json

status_route = Blueprint('status', __name__)

@status_route.route('/status')
def status():
    result = {
        'status': 'OK'
    }

    return json.dumps(result)
