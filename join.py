﻿import os

from google.appengine.ext import db

import logging
import webapp2
import json


from api import hitapi, wlnet
from main import *
from players import Player
from wtforms import *
import lot



class JoinPage(BaseHandler):
  def get(self, lotID):
    if 'authenticatedtoken' not in self.session:
      return self.redirect('http://' + wlnet + "/CLOT/Auth?p=62456969&state=join/" + str(long(lotID)))

    container = lot.getLot(lotID)
    inviteToken = self.session['authenticatedtoken']

    #Call the warlight API to get the name, color, and verify that the invite token is correct
    apiret = hitapi('/API/ValidateInviteToken', { 'Token':  inviteToken })

    if not "tokenIsValid" in apiret:
      return self.response.write('The supplied invite token is invalid.  Please contact the CLOT author for assistance.')

    #Check if this invite token is new to us
    player = Player.query(Player.inviteToken == inviteToken).get()
    if player is None:
      data = json.loads(apiret)
      player = Player(inviteToken=inviteToken, name=data['name'], color=data['color'])
      player.put()
      logging.info("Created player " + unicode(player))

    #Set them as participating in the current lot
    addIfNotPresent(container.lot.playersParticipating, player.key.id())
    container.players[player.key.id()] = player
    container.lot.put()
    container.changed()
    logging.info("Player " + unicode(player) + " joined " + unicode(container.lot))

    self.response.write(get_template('join.html').render({ 'container': container }))