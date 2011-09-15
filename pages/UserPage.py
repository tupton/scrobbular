import cgi
import scrobble

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class UserPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            session_key = scrobble.get_session_key(user)
            if session_key:
                secret = scrobble.get_secret(user)
                self.response.out.write(template.render('templates/user.html',
                    {
                        'user': user.email(),
                        'secret': secret,
                        'logout': users.create_logout_url('/'),
                        'styles': ['user'],
                        'scripts': ['user']
                    }
                ))
            else:
                self.response.out.write(template.render('templates/user.html',
                    {
                        'user': user.email(),
                        'logout': users.create_logout_url('/'),
                        'styles': ['user'],
                        'scripts': ['user']
                    }
                ))
        else:
            self.redirect(users.create_login_url('/user'))

