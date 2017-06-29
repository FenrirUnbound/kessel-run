import googlemaps
import json

from flask import Blueprint
from models.route import Route
from models.secret import Secret
from models.timing import Timing

route_data = Route()
timings_route = Blueprint('timings', __name__)

def pull_data(map_data):
    element = map_data['rows'].pop()
    matrix_data = element['elements'].pop()

    return {
        'distance': matrix_data['distance']['text'],
        'duration': matrix_data['duration']['value']
    }

@timings_route.route('/timings/<int:route_id>')
def measure_timing(route_id):
    route = route_data.get(route_id - 1)
    token = Secret.token()
    gmaps = googlemaps.Client(key=token)

    map_data = gmaps.distance_matrix(
        origins=route['origin'],
        destinations=route['destination'],
        mode='driving',
        units='imperial'
        )
    result = pull_data(map_data)

    Timing(distance=result['distance'], duration=result['duration']).put()

    return '', 204
