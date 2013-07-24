import os

from google.appengine.ext import db

import logging
import webapp2
from main import *

from players import Player
from games import GamePlayer
from games import Game

class HomePage(webapp2.RequestHandler):
  def get(self):

    #Check if we need to do first-time setup
    if ClotConfig.all().count() == 0 and not api.TestMode:
      return self.redirect('/setup')

    #Gather data used by home.html
    players = Player.all()
    playersDict = dict([(p.key().id(),p) for p in players])

    gamePlayers = group(GamePlayer.all(), lambda z: z.gameID)
    games = Game.all()

    self.response.write(get_template('home.html').render({ 'players': players, 'games': games}))
