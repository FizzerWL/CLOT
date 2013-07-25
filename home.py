import os

from google.appengine.ext import ndb
from google.appengine.api import memcache

import logging
import webapp2
from main import *

from players import Player
from games import Game
import lot

class HomePage(webapp2.RequestHandler):
  def get(self):

    cache = memcache.get('home')
    #if cache is not None:
    #    return self.response.write(cache)

    #Check if we need to do first-time setup
    if getClotConfig() is None:
      return self.redirect('/setup')

    html = get_template('home.html').render({ 'lots': list(lot.LOT.query()) })

    if not memcache.add('home', html):
      logging.info("Memcache add failed")

    self.response.write(html)
