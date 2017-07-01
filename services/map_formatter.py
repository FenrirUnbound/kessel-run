class MapFormatter(object):
    def __init__(self):
        self.formatter = Filter(
            next=Result()
            )

    def format(self, content):
        return self.formatter.format(content=content)

class AbstractFormatter(object):
    def __init__(self, next):
        self.next = next

    def format(self, content):
        result = self._format(content=content)

        if self.next:
            return self.next.format(content=result)
        else:
            return result

    def _format(self, content):
        raise Error('Not implemented')

class Filter(AbstractFormatter):
    def __init__(self, next=None):
        self.next = next

    def _format(self, content):
        # be greedy & give first route
        # todo: filter based on route name/summary
        return content[0]

class Result(AbstractFormatter):
    def __init__(self, next=None):
        self.next = next

    def _format(self, content):
        direction_data = content['legs'][0]

        return {
            'distance': direction_data['distance']['text'],
            'duration': direction_data['duration_in_traffic']['value']
        }
