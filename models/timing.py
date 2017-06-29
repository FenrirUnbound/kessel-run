from google.appengine.ext import ndb

class Timing(ndb.Model):
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    distance = ndb.StringProperty()
    duration = ndb.IntegerProperty()
