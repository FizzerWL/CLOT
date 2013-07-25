import os
import webapp2
import logging
from api import TestMode
from main import *

from players import Player
from games import Game
from datetime import datetime, date
import cron
import random
import string

class TestPage(webapp2.RequestHandler):

  def renderPage(self, message):
    
    players = Player.query()
    playersDict = dict([(p.key.id(),p) for p in players])
    games = Game.query()

    self.response.write(get_template('test.html').render({  'players': players, 'games': games, 'message': message }))


  def get(self):

    if not TestMode:
      return self.response.write("api.TestMode is not enabled.  This page should only be used while testing.")

    TestPage.renderPage(self, '')

  def post(self):
    if 'ClearData' in self.request.POST:
      #User clicked Clear Data, delete all games and players
      ndb.delete_multi([o.key for o in Game.query()])
      ndb.delete_multi([o.key for o in Player.query()])
      TestPage.renderPage(self, 'Deleted all games and players')

    elif 'RunCron' in self.request.POST:
      #Just execute the same thing that we'd do if we hit /cron, but also time it
      start = datetime.now()
      cron.execute()
      TestPage.renderPage(self, 'Cron finished in ' + unicode(datetime.now() - start))
    
    elif 'AddPlayers' in self.request.POST:
      #Add some dummy player data. It won't work on warlight.net of course, but if TestMode is enabled it won't ever be passed there.   Just be sure and delete it before disabling TestMode.
      numPlayers = int(self.request.POST["NumPlayers"])
      
      for z in range(numPlayers):
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
        Player(name=name, inviteToken=name, color="#0000FF").put()
      
      TestPage.renderPage(self, 'Added ' + str(numPlayers) + ' fake players')

    elif 'Test' in self.request.POST:

      #Just a blank space for testing random stuff
      
      
      TestPage.renderPage(self, 'Ran test code')

    else:
      self.response.write("No handler")

    