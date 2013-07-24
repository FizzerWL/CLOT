import os

from google.appengine.ext import ndb
import webapp2


class Player(ndb.Model):
  name = ndb.StringProperty()
  inviteToken = ndb.StringProperty(required=True)
  color = ndb.StringProperty()
  isParticipating = ndb.BooleanProperty(default=True)
  currentRank = ndb.IntegerProperty(default=0)
  created = ndb.DateTimeProperty(auto_now_add=True)
  modified = ndb.DateTimeProperty(auto_now=True)

  def __repr__(self):
    return str(self.key.id()) + " " + self.name
