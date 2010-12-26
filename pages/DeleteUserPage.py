import scrobble

from google.appengine.api import users
from google.appengine.ext import webapp

class DeleteUserPage(webapp.RequestHandler):
    """Handle a request to delete a user"""

    def post(self):
        user = users.get_current_user()

