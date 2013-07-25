import os

from google.appengine.ext import ndb
import json

import logging

class Game(ndb.Model):
  """Represents a game.  This has its own ID local to the CLOT, but it also stores wlnetGameID which is the ID of the game on WarLight.net.
  This also stores a winner field which contains a playerID only if the game is finished.
  The __repr__ function is just used for debugging."""

  players = ndb.IntegerProperty(repeated=True)
  winner = ndb.IntegerProperty()
  wlnetGameID = ndb.IntegerProperty(required=True)
  name = ndb.StringProperty()
  dateCreated = ndb.DateTimeProperty(auto_now_add=True)
  dateEnded = ndb.DateTimeProperty()

  def __repr__(self):
    return str(self.key.id()) + ", wlnetGameID=" + str(self.wlnetGameID) + ", players=" + unicode(self.players)


def createGame(players, templateID):
  """This calls the WarLight.net API to create a game, and then creates the Game rows in the local DB"""
  gameName = ' vs '.join([p.name for p in players])[:50]

  config = getClotConfig()
  apiRetStr = postToApi('/API/CreateGame', json.dumps( { 
                               'hostEmail': config.adminEmail, 
                               'hostAPIToken': config.adminApiToken,
                               'templateID': templateID,
                               'gameName': gameName,
                               'personalMessage': '',
                               'players': [ { 'token': p.inviteToken, 'team': 'None' } for p in players]
                               }))
  apiRet = json.loads(apiRetStr)

  gid = int(apiRet.get('gameID', -1))
  if gid == -1:
    raise Exception("CreateGame returned error: " + apiRet.get('error', apiRetStr))

  g = Game(wlnetGameID=gid, name=gameName)
  g.players = [p.key.id() for p in players]
  g.put()

  logging.info("Created game " + str(g.key.id()) + " '" + gameName + "', wlnetGameID=" + str(gid))

  return g

from api import postToApi
from api import hitapi
from main import getClotConfig
from players import Player
