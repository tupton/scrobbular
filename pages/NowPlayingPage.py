import cgi
import scrobble
import pages

class NowPlayingPage(pages.LastfmRequestPage):
    """Handle a request to update the now playing status"""

    required_params = ['username', 'artist', 'track']
    optional_params = ['album', 'duration']

    def post(self):
        params = self.get_params()

        if not params:
            return

        api = scrobble.LastfmApi(params['username'])
        api.update_now_playing(params['track'], params['artist'], params['duration'], params['album'])
        
