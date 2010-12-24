import cgi
import scrobble

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class ScrobblePage(webapp.RequestHandler):
    """Handle requests to scrobble a track"""
    required_params = ['username', 'artist', 'track', 'duration']
    optional_params = ['album']

    def post(self):
        params = self.get_params()

        if not params:
            return

        self.response.out.write(cgi.escape("\n".join([k + '=' + v for (k,v) in params.iteritems()])))

        api = LastfmApi(params['username'])
        api.scrobble(params['track'], params['artist'], params['duration'], params['album'])
        
    def get_params(self):
        """Get the parameters after verifying them"""
        # Required parameters
        required = dict()
        for r in self.required_params:
            required[r] = self.request.get(r)

        # Optional parameters
        optional = dict()
        for o in self.optional_params:
            optional[o] = self.request.get(o) 

        if not required['username'] or not required['artist'] or not required['track'] or not required['duration']:
            self.response.set_status(400)
            required_arguments = "\n".join([a + '=' + self.request.get(a) for a in self.required_params])
            optional_arguments = "\n".join([a + '=' + self.request.get(a) for a in self.optional_params])

            self.response.out.write(cgi.escape("Incorrect arguments were supplied:" +
                "\n\nRequired:\n" + required_arguments + "\n\nOptional:\n" + optional_arguments))
            return None

        return dict([[a, self.request.get(a)] for a in self.request.arguments()])
