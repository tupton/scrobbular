import cgi
import scrobble

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class UserPage(webapp.RequestHandler):
    def get(self):
        path = self.request.path
        if len(path) > len('/user/'):
            user = path[len('/user/'):].split('/')[0] 
            session_key = None
            if user:
                session_key = scrobble.get_session_key(user)
            self.response.out.write(template.render('templates/user.html', {'username': user,
                                                                            'session_key': session_key}))
        else:
            self.response.out.write("<br/>".join(['url: ' + self.request.url,
                                                'path: ' + self.request.path,
                                                'query_string: ' + self.request.query_string]))

