import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class HowtoPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/howto.html', {'styles': ['howto']}))

