
from google.appengine.ext import db

import httplib
import urllib
import os
import jinja2

from itertools import groupby


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

def get_template(name):
  return JINJA_ENVIRONMENT.get_template('templates/' + name)

class ClotConfig(db.Model):
  adminEmail = db.StringProperty(required=True)
  adminApiToken = db.StringProperty(required=True)


def getClotConfig():
  if api.TestMode:
    return ClotConfig(adminEmail='bogus', adminApiToken='bogus') #return a bogus one while we're in test mode. It'll never be used.

  for c in ClotConfig.all():
      return c



def group(collection, keyfunc):
  data = sorted(collection, key=keyfunc)
  ret = {}
  for k,g in groupby(data, keyfunc):
    ret[k] = list(g)
  return ret

import api
