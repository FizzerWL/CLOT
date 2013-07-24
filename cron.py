import os

from google.appengine.ext import db

import datetime
import logging
import json
import webapp2

from clot import createGames
from clot import setRanks
from games import Game
from api import hitapi
from players import Player


class CronPage(webapp2.RequestHandler):
  def get(self):
    execute()
    self.response.write("Cron complete")

def execute():
  logging.info("Starting cron...")
  checkInProgressGames()
  createGames()
  setRanks()
  logging.info("Cron done")

def checkInProgressGames():
  """This is called periodically to look for games that are finished.  If we find a finished game, we record the winner"""

  #Find all games that we think aren't finished
  activeGames = Game.query(Game.winner == None)

  for g in activeGames:
    #call WarLight's GameFeed API so that it can tell us if it's finished or not
    apiret = hitapi('/API/GameFeed?GameID=' + str(g.wlnetGameID), {})
    data = json.loads(apiret)
    state = data.get('state', 'err')
    if state == 'err': raise Exception("GameFeed API failed.  Message = " + data.get('error', apiret))

    if state == 'Finished':
      #It's finished. Record the winner and save it back.
      winner = findWinner(data)
      logging.info('Identified the winner of game ' + str(g.wlnetGameID) + ' is ' + unicode(winner))
      g.winner = winner.key.id()
      g.dateEnded = datetime.datetime.now()
      g.put()
    else:
      #It's still going.
      logging.info('Game ' + str(g.wlnetGameID) + ' is not finished, state=' + state + ', numTurns=' + data['numberOfTurns'])

def findWinner(data):
  """Simple helper function to return the Player who won the game.  This takes json data returned by the GameFeed 
  API.  We just look for a player with the "won" state and then retrieve their Player instance from the database"""
  winnerInviteToken = filter(lambda p: p['state'] == 'Won', data['players'])[0]["id"]
  return Player.query(Player.inviteToken == winnerInviteToken).get()

