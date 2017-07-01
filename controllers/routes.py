from flask import Blueprint, Response
from models.route import Route
from models.timing import Timing

import json

route_data = Route()
routes_route = Blueprint('routes', __name__)

def reply_payload(payload, status_code=200):
    result = {
        'data': payload
    }

    body = json.dumps(result)

    return Response(body, status=status_code, mimetype='application/json')

@routes_route.route('/routes')
def list_routes():
    result = []

    for i in range(1):
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
    timing_data = Timing.get_past_day()
    result = []
    for datapoint in timing_data:
        result.append({
            'distance': datapoint.distance,
            'duration': datapoint.duration,
            'timestamp': datapoint.create_time.strftime('%s')
        })

    return reply_payload(result)
