import cgi
import scrobble

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class SubmitPage(webapp.RequestHandler):
    def post(self):
        #self.response.out.write(cgi.escape("\n".join([a + '=' + self.request.get(a) for a in self.request.arguments()])))
        username = self.request.get('username', None)
        session_key = self.request.get('session_key', None)
        if username is not None and session_key is not None:
            scrobble.put_session_key(username, session_key)
            self.response.out.write(cgi.escape('Set session key for %s to %s (received key: %s)' % \
                (username, scrobble.get_session_key(username), session_key)))

    def get(self):
        self.response.out.write(template.render('templates/submit.html', {}))

