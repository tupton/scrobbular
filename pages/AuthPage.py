import cgi
import scrobble
import time

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AuthPage(webapp.RequestHandler):
    def post(self):
        username = self.request.get('username')
        session_key = scrobble.get_session_key(username)
        if session_key is None:
            api = scrobble.LastfmApi(username)
            self.redirect(api.get_request_token_url())
        else:
            self.redirect('/user/' + username)

    def get(self):
        username = self.request.get('username')
        token = self.request.get('token')
        if username and token:
            api = scrobble.LastfmApi(username)
            session_key = api.create_and_set_session_key(token)
            self.redirect('/user/' + username)

