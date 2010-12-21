import cgi
import scrobble

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class ScrobblePage(webapp.RequestHandler):
    """Handle requests to scrobble a track"""

    def post(self):
        # Required parameters
        required_params = ['user', 'artist', 'track', 'duration']
        required = dict()
        for r in required_params:
            required[r] = self.request.get(r)

        # Optional parameters
        optional_params = ['album']
        optional = dict()
        for o in optional_params:
            optional[o] = self.request.get(o) 

        if not required['user'] or not required['artist'] or not required['track'] or not required['duration']:
            # TODO set error code for not enough args
            self.response.set_status(400)
            required_arguments = "\n".join([a + '=' + self.request.get(a) for a in required_params])
            optional_arguments = "\n".join([a + '=' + self.request.get(a) if a not in required_params else '' for a in self.request.arguments()])

            self.response.out.write(cgi.escape("Incorrect arguments were supplied:" +
                "\n\nRequired:\n" + required_arguments + "\n\nOptional:\n" + optional_arguments))
            return

        self.response.out.write('You gave me everything I wanted')
        
