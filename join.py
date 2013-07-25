import os

from google.appengine.ext import db

import logging
import webapp2
import json


from api import hitapi
from main import *
from players import Player
from wtforms import *
import lot


class JoinForm(Form):
  inviteToken = TextField('Invite token', [validators.required()])


class JoinPage(webapp2.RequestHandler):
  def get(self, lotID):
    self.response.write(get_template('join.html').render({ 'form': JoinForm(), 'container': lot.getLot(lotID) }))

  def post(self, lotID):

    container = lot.getLot(lotID)

    form = JoinForm(self.request.POST)

    if not form.validate():
      return self.response.write("You must enter an invite token")
      

    inviteToken = form.inviteToken.data

    #Call the warlight API to get the name, color, and verify that the invite token is correct
    apiret = hitapi('/API/ValidateInviteToken', { 'Token':  inviteToken })

    if not "tokenIsValid" in apiret:
      return self.response.write('The supplied invite token is invalid. Please ensure you copied it from WarLight.net correctly.')

    #Ensure this invite token doesn't already exist
    player = Player.query(Player.inviteToken == inviteToken).get()
    if player is None:
      data = json.loads(apiret)
      player = Player(inviteToken=inviteToken, name=data['name'], color=data['color'])
      player.put()
      logging.info("Created player " + unicode(player))

    #Set them as participating in the current lot
    addIfNotPresent(container.lot.playersParticipating, player.key.id())
    container.lot.put()
    container.changed()
    logging.info("Player " + unicode(player) + " joined " + unicode(container.lot))
  
    return self.redirect('/player/' + str(player.key.id()))