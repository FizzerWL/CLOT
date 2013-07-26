import os
import webapp2

from google.appengine.ext import db

from api import hitapi
from main import *
from games import Game
from players import Player
import lot


class ViewLotPage(BaseHandler):
  def get(self, lotID):
    container = lot.getLot(lotID)
    self.response.write(get_template('viewlot.html').render({'container': container, 'lotrendered': container.render() }))

