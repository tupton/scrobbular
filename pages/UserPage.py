import cgi
import scrobble

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class UserPage(webapp.RequestHandler):
    def get(self):
        user = self.get_username_from_path()
        if user:
            self.render_user_page(user)
        else:
            self.redirect('/')

    def get_username_from_path(self):
        """Get the username from the path that was used to request this page"""
        user = None
        path = self.request.path
        if len(path) > len('/user/'):
            user = path[len('/user/'):].split('/')[0] 
        return user

    def render_user_page(self, user):
        """Render the user page for the given user"""
        session_key = scrobble.get_session_key(user)
        self.response.out.write(template.render('templates/user.html', {'username': user,
                                                                        'session_key': session_key,
                                                                        'styles': ['user']
                                                                       }))

