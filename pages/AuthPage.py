import cgi
import scrobble
import time

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AuthPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            user_id = user.user_id()
            session_key = scrobble.get_session_key(user_id)
            if session_key is None:
                api = scrobble.LastfmApi(user_id)
                self.redirect(api.get_request_token_url())
            else:
                self.redirect('/user')
        else:
            self.redirect(users.create_login_url('/'))

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        token = self.request.get('token')
        if token:
            api = scrobble.LastfmApi(user.user_id())
            session_key = api.create_and_set_session_key(token)
            self.redirect('/user')

