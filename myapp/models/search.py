from google.appengine.ext import ndb


class Search(ndb.Model):
    city = ndb.StringProperty()
    counter = ndb.IntegerProperty(default=0)