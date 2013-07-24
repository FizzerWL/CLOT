import os

from google.appengine.ext import db
import webapp2


class Player(db.Model):
  name = db.StringProperty()
  inviteToken = db.StringProperty(required=True)
  color = db.StringProperty()
  isParticipating = db.BooleanProperty(default=True, required=True)
  currentRank = db.IntegerProperty(default=0, required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)

  def __repr__(self):
    return str(self.key().id()) + " " + self.name
