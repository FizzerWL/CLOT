import os

from google.appengine.ext import ndb

import logging
import httplib
import urllib
import urlparse

from random import randint
import json



TestMode = True  #If you enable TestMode here, all calls to the WarLight API that your code
                 # makes will be intercepted and dummy data will be returned.  This is useful
                 # for testing your code before you release it to the public.  Make sure to 
                 # change this back to False before releasing your app.


#wlnet = 'warlight.net'
wlnet = '192.168.1.105:81'

  

def hitapi(api, params):
  config = getClotConfig()
  return hitapiwithauth(api, params, config.adminEmail, config.adminApiToken)
  
def hitapiwithauth(api, params, email, apitoken):
  prms = { 'Email': email, 'APIToken': apitoken }
  prms.update(params)

  return postToApi(api, urllib.urlencode(prms))

def postToApi(api, postData):  
  #logging.info("POSTing to " + wlnet + api + ", data=" + postData)

  if TestMode:
    return testModeApi(api, postData)
  else:
    conn = httplib.HTTPConnection(wlnet, 80)
    conn.connect()
    request = conn.putrequest('POST', api)
    conn.send(postData)
    resp = conn.getresponse()
    ret = resp.read()

    conn.close()
    return ret

def testModeApi(api, postData):

  postDataDict = urlparse.parse_qs(postData)

  if api == '/API/CreateGame':
    #When we simulate CreateGame, we just return a random game ID.  We assume the caller is going to write this into the local Game table.  TODO: query the local Game table to eliminate the tiny chance that we generate an ID already in use
    return json.dumps({ "gameID": randint(0, 2000000000)})

  elif api.startswith('/API/GameFeed?GameID='):
    #When we simulate GameFeed, always return that the game is finished. Pick a winner randomly.  We access the Game table to find out which players are involved
    wlnetGameID = long(api[21:])
    game = Game.query(Game.wlnetGameID == wlnetGameID).get()
    players = ndb.get_multi([ ndb.Key(Player, p) for p in game.players])
    winner = players[randint(0, len(players) - 1)] #pick a winner randomly

    return json.dumps({ "id": wlnetGameID, "state": "Finished", "name": game.name, "numberOfTurns": randint(7, 14), 
                     "players": [{ "id": p.inviteToken, "isAI": "False", "state": "Won" if p == winner else "SurrenderAccepted" } for p in players] })

  elif api == '/API/ValidateInviteToken':

    return json.dumps({ "tokenIsValid": "", "name": "Fake " + postDataDict["Token"][0], "isMember": "True", "color": "#FF0000", "tagline": "Fake player created by TestMode=True", "clotpass": "fake" })
  else:
    raise Exception("No test handler for api " + api)



from main import getClotConfig
from games import Game
from players import Player

