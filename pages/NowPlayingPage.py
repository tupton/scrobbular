import cgi
import scrobble
import pages

from google.appengine.api import users

class NowPlayingPage(pages.LastfmRequestPage):
    """Handle a request to update the now playing status"""

    required_params = ['username', 's', 'artist', 'track']
    optional_params = ['album', 'duration']

    def post(self):
        params = self.get_params()

        if not params:
            return

        user = users.User(params['username'])
        api = scrobble.LastfmApi(user, params['s'])
        api.update_now_playing(params['track'], params['artist'], params['duration'], params['album'])
        
