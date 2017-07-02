from datetime import datetime, timedelta
from flask import Blueprint, Response
from models.route import Route
from models.timing import Timing

import json

route_data = Route()
routes_route = Blueprint('routes', __name__)

CACHE_LIFETIME = timedelta(minutes=5)
CACHE = {}

def check_cache(route_id):
    # nothing in cache
    if route_id not in CACHE:
        return None

    result = CACHE[route_id]

    # check expired value
    if datetime.now() > result['expire_time']:
        return None

    return result['data']

def save_cache(route_id, data):
    expire_time = datetime.now() + CACHE_LIFETIME

    CACHE[route_id] = {
        'data': data,
        'expire_time': expire_time
    }

def reply_payload(payload, status_code=200):
    result = {
        'data': payload
    }

    body = json.dumps(result)

    return Response(body, status=status_code, mimetype='application/json')

@routes_route.route('/routes')
def list_routes():
    result = []

    for i in range(route_data.size):
        item = {
            'id': i + 1
        }

        item.update(route_data.get(i))
        result.append(item)

    return reply_payload(result)

@routes_route.route('/routes/<int:route_id>')
def get_route(route_id):
    if route_id <= 0 or route_id > route_data.size:
        return '', 404

    result = route_data.get(route_id - 1)
    result['id'] = route_id

    return reply_payload(result)


@routes_route.route('/routes/<int:route_id>/day')
def get_day_timings(route_id):
    cached_result = check_cache(route_id=route_id)
    if cached_result is not None:
        return reply_payload(payload=cached_result)

    timing_data = Timing.get_past_day(route_id=route_id)
    result = []
    for datapoint in timing_data:
        result.append({
            'distance': datapoint.distance,
            'duration': datapoint.duration,
            'timestamp': datapoint.create_time.strftime('%s')
        })

    save_cache(route_id=route_id, data=result)

    return reply_payload(result)
