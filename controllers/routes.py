from flask import Blueprint
from models.route import Route
from models.timing import Timing

import json

route_data = Route()
routes_route = Blueprint('routes', __name__)

@routes_route.route('/routes')
def list_routes():
    data = []

    for i in range(1):
        item = {
            'id': i + 1
        }

        item.update(route_data.get(i))
        data.append(item)

    result = {
        'data': data
    }

    return json.dumps(result)

@routes_route.route('/routes/<int:route_id>')
def get_route(route_id):
    if route_id <= 0 or route_id > route_data.size:
        return '', 404

    data = route_data.get(route_id - 1)
    data['id'] = route_id

    result = {
        'data': data
    }

    return json.dumps(result)


@routes_route.route('/routes/<int:route_id>/day')
def get_day_timings(route_id):
    timing_data = Timing.get_past_day()
    data = []
    for datapoint in timing_data:
        data.append({
            'distance': datapoint.distance,
            'duration': datapoint.duration
        })

    result = {
        'data': data
    }

    return json.dumps({ 'data': data }), 200
