import logging
import webapp2
import datetime

from wtforms import *
from main import *
import lot

class FinishLotPage(BaseHandler):
  def get(self, lotID):
    container = lot.getLot(lotID)
    container.lot.dateEnded = datetime.datetime.now()
    container.lot.playersParticipating = []
    container.lot.put()
    container.changed()

    logging.info('LOT ended')

    self.redirect('/')


