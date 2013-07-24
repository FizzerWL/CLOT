import os

from google.appengine.ext import db

import logging
import webapp2


from wtforms import *
from main import *
from players import Player


class LeaveForm(Form):
  inviteToken = TextField("Invite Token", [validators.required()])

class LeavePage(webapp2.RequestHandler):
  def get(self):
    self.response.write(get_template('leave.html').render({ 'form': LeaveForm() }))

  def post(self):

    form = LeaveForm(self.request.POST)

    if not form.validate():
      return self.response.write("Please enter your invite token")


    inviteToken = form.inviteToken.data

    #Find the player by their token
    player = Player.query(Player.inviteToken == inviteToken).get()
    if not player:
      return self.response.write("Invite token is invalid")

    #When they leave, just set their isParticipating to false
    player.isParticipating = False
    player.put()

    logging.info("Player left ladder " + unicode(player))
    self.redirect('/player/' + str(player.key.id()))

