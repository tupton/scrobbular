import cgi
import scrobble

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class UserPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            user_id = user.user_id()
            session_key = scrobble.get_session_key(user_id)
            if session_key:
                secret = scrobble.get_secret(user_id)
                self.response.out.write(template.render('templates/user.html', {'secret': secret,
                                                                                'logout': users.create_logout_url('/'),
                                                                                'styles': ['user'],
                                                                                'scripts': ['user']
                                                                               }))
            else:
                self.response.out.write(template.render('templates/user.html', {'logout': users.create_logout_url('/'),
                                                                                'styles': ['user'],
                                                                                'scripts': ['user']
                                                                               }))
        else:
            self.redirect(users.create_login_url('/user'))

    def post(self):
        """Handle a post request to the user page"""
        user = users.get_current_user()
        secret = self.request.get('secret')
        if user and secret:
            scrobble.put_secret(user.user_id(), secret)
            self.redirect('/user')
        else:
            self.redirect('/')
