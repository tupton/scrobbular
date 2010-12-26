import scrobble

from google.appengine.api import users
from google.appengine.ext import webapp

class ChangeSecretPage(webapp.RequestHandler):
    """Handle a request to change a secret for a user"""

    def post(self):
        user = users.get_current_user()
        secret = self.request.get('secret')
        if user and secret:
            scrobble.put_secret(user, secret)
            self.redirect('/user')
        else:
            self.redirect('/')
