import os

class Secret(object):
    @staticmethod
    def token():
        token = os.ENVIRON['TOKEN']

        return token if len(token) > 0 else ''
