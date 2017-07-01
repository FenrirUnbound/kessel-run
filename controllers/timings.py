import json

from flask import Blueprint
from models.timing import Timing
from services.gmaps import Gmaps

timings_route = Blueprint('timings', __name__)

@timings_route.route('/timings/<int:route_id>')
def measure_timing(route_id):
    google_maps = Gmaps()
    result = google_maps.lookup_travel_time(route_id=route_id-1)

    Timing(distance=result['distance'], duration=result['duration']).put()

    return '', 204
