import webapp2

from setup import SetupPage
from home import HomePage
from join import JoinPage
from viewplayer import PlayerPage
from leave import LeavePage
from cron import CronPage
from test import TestPage

application = webapp2.WSGIApplication([
    ('/setup', SetupPage),
    ('/', HomePage),
    ('/join', JoinPage),
    ('/leave', LeavePage),
    ('/player/(\d+)', PlayerPage),
    ('/cron', CronPage),
    ('/test', TestPage),
], debug=True)