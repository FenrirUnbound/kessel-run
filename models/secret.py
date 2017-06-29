import os

class Secret(object):
    @staticmethod
    def token():
        return os.getenv('TOKEN', '')
