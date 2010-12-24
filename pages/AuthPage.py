import cgi
import scrobble
import time

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AuthPage(webapp.RequestHandler):
    def post(self):
        username = self.request.get('username', None)
        session_key = scrobble.get_session_key(username)
        if session_key is None:
            api = scrobble.LastfmApi(username)
            self.redirect(api.get_request_token_url())
        else:
            # TODO
            self.response.out.write(cgi.escape('already authenticated ' + username + ': ' + session_key))

    def get(self):
        username = self.response.get('username')
        token = self.response.get('token')
        if user and token:
            api = scrobble.LastfmApi(username)
            session_key = api.create_and_session_key(token)
            # TODO
            self.response.out.write('session key set for ' + username + ': ' + session_key)
