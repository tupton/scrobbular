import cgi
import scrobble
import pages

from google.appengine.api import users

class ScrobblePage(pages.LastfmRequestPage):
    """Handle requests to scrobble a track"""
    required_params = ['username', 's', 'artist', 'track', 'duration']
    optional_params = ['album']

    def post(self):
        params = self.get_params()

        if not params:
            return

        user = users.User(params['username'])
        api = scrobble.LastfmApi(user, params['s'])
        api.scrobble(params['track'], params['artist'], params['duration'], params['album'])
        
