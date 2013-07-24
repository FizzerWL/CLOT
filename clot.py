import os

from google.appengine.ext import db

import logging
import random
import json

from games import Game
from games import GamePlayer
from games import createGame
from players import Player
from main import group

def createGames():
  """This is called periodically to check for new games that need to be created.  
  You should replace this with your own logic for how games are to be created.
  Right now, this function just randomly pairs up players who aren't in a game."""

  #Retrieve all games that are ongoing
  activeGames = list(Game.query(Game.winner == None))
  activeGameIDs = dict([[g.key.id(), g] for g in activeGames])
  logging.info("Active games: " + unicode(activeGameIDs))

  #Throw all of the player IDs that are in these ongoing games into a dictionary
  playerIDsInGames = dict([[gp.playerID, gp] for gp in GamePlayer.query() if gp.gameID in activeGameIDs])

  #Find all players who aren't in the dictionary (and therefore aren't in any games) and also have not left the CLOT (isParticipating is true)
  allPlayers = Player.query()
  playersNotInGames = [p for p in allPlayers if p.isParticipating and p.key.id() not in playerIDsInGames]
  logging.info("Players not in games: " + ','.join([unicode(p) for p in playersNotInGames]))

  #Randomize the order
  random.shuffle(playersNotInGames)

  #The template ID defines the settings used when the game is created.  You can create your own template on warlight.net and enter its ID here
  templateID = 251301

  #Create a game for everyone not in a game.
  gamesCreated = [createGame(pair, templateID) for pair in pairs(playersNotInGames)]
  logging.info("Created games " + unicode(','.join([unicode(g) for g in gamesCreated])))

def pairs(lst):
  """Simple helper function that groups a list into pairs.  For example, [1,2,3,4,5] would return [1,2],[3,4]"""
  for i in range(1, len(lst), 2):
    yield lst[i-1], lst[i]

def setRanks():
  """This looks at what games everyone has won and sets their currentRank field.
  The current algorithm is very simple - just award ranks based on number of games won.
  You should replace this with your own ranking logic."""

  #Load all finished games
  finishedGames = Game.query(Game.winner != None)

  #Group them by who won
  finishedGamesGroupedByWinner = group(finishedGames, lambda g: g.winner)

  #Get rid of the game data, and replace it with the number of games each player won
  winCounts = dict(map(lambda (playerID,games): (playerID, len(games)), finishedGamesGroupedByWinner.items())) 

  #Map this from Player.query() to ensure we have an entry for every player, even those with no wins
  playersMappedToNumWins = [(p, winCounts.get(p.key.id(), 0)) for p in Player.query()] 

  #sort by the number of wins each player has.
  playersMappedToNumWins.sort(key=lambda (player,numWins): numWins, reverse=True)

  #Now that it's sorted, we can just loop through each player and set their currentRank
  for index,(player,numWins) in enumerate(playersMappedToNumWins):
    player.currentRank = index + 1 #index is 0-based, and we want our top player to be ranked #1, so we add one.
    player.put()

  logging.info('setRanks finished')

