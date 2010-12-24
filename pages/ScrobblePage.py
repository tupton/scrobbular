import cgi
import scrobble
import pages

class ScrobblePage(pages.LastfmRequestPage):
    """Handle requests to scrobble a track"""
    required_params = ['username', 'artist', 'track', 'duration']
    optional_params = ['album']

    def post(self):
        params = self.get_params()

        if not params:
            return

        api = scrobble.LastfmApi(params['username'])
        api.scrobble(params['track'], params['artist'], params['duration'], params['album'])
        
