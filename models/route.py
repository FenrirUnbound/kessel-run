import os
import yaml

ORIGIN = '701 1st Avenue, Sunnyvale, CA 94089'

class Route(object):
    def __init__(self):
        filename = os.path.join(os.path.dirname(__file__), 'route_data.yaml')
        with open(filename, 'r') as f:
            route_data = yaml.load(f)

            self.routes = route_data['routes']

        self.size = len(self.routes)

        for i in range(self.size):
            self.routes[i].update({ 'origin': ORIGIN })

    def get(self, route_id):
        if route_id < 0 or route_id > self.size:
            route_id = 0

        return self.routes[route_id]

    def size(self):
        return self.size
