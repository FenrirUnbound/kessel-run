import googlemaps
import time

from map_formatter import MapFormatter
from models.route import Route
from models.secret import Secret

class Gmaps(object):
    def __init__(self):
        self.gmaps = googlemaps.Client(key=Secret.token())
        self.route_data = Route()
        self.formatter = MapFormatter()

    def lookup_travel_time(self, route_id):
        desired_route = self.route_data.get(route_id)
        now = int(time.time())

        map_data = self.gmaps.directions(
            alternatives=True,
            departure_time=now,
            destination=desired_route['destination'],
            mode='driving',
            origin=desired_route['origin'],
            units='imperial'
            )

        return self.formatter.format(content=map_data)
