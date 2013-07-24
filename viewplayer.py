import os
import webapp2

from google.appengine.ext import db

from api import hitapi
from main import *
from games import GamePlayer
from games import Game
from players import Player


class PlayerPage(webapp2.RequestHandler):
  def get(self, playerID):
    playerID = int(playerID)
    p = Player.get_by_id(playerID)
    gameIDs = [g.gameID for g in GamePlayer.query(GamePlayer.playerID == playerID)]
    games = ndb.get_multi(gameIDs)
    self.response.write(get_template('viewplayer.html').render({'player': p, 'games': games}))

