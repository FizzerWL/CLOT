import os

from google.appengine.ext import db

import logging
import webapp2


from api import hitapi
from main import *
from players import Player
from wtforms import *
import json


class JoinForm(Form):
  inviteToken = TextField('Invite token', [validators.required()])


class JoinPage(webapp2.RequestHandler):
  def get(self):
    self.response.write(get_template('join.html').render({ 'form': JoinForm() }))

  def post(self):

    form = JoinForm(self.request.POST)

    if not form.validate():
      return self.response.write("You must enter an invite token")
      

    inviteToken = form.inviteToken.data

    #Call the warlight API to get the name, color, and verify that the invite token is correct
    apiret = hitapi('/API/ValidateInviteToken', { 'Token':  inviteToken })

    if not "tokenIsValid" in apiret:
      return self.response.write('The supplied invite token is invalid. Please ensure you copied it from WarLight.net correctly.')

    #Ensure this invite token doesn't already exist
    existing = Player.query(Player.inviteToken == inviteToken).get()
    if existing:
      #If someone tries to join when they're already in the DB, just set their isParticipating flag back to true
      existing.isParticipating = True
      existing.put()
      return self.redirect('/player/' + str(existing.key.id()))

    data = json.loads(apiret)
    player = Player(inviteToken=inviteToken, name=data['name'], color=data['color'])


    player.put()
    logging.info("Created player " + unicode(player))
  
    return self.redirect('/player/' + str(player.key.id()))