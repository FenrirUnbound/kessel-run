
from datetime import datetime, timedelta
from google.appengine.ext import ndb

MAX_FETCH = (60 / 10) * 24

class Timing(ndb.Model):
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    distance = ndb.StringProperty()
    duration = ndb.IntegerProperty()

    @classmethod
    def get_past_day(cls):
        now = datetime.now() - timedelta(days=1)

        return Timing.query(Timing.create_time > now).order(-Timing.create_time).fetch(MAX_FETCH)
