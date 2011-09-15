from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import pages

application = webapp.WSGIApplication(
                                     [('/', pages.IndexPage),
                                      ('/auth', pages.AuthPage),
                                      ('/howto', pages.HowtoPage),
                                      ('/now_playing', pages.NowPlayingPage),
                                      ('/user', pages.UserPage),
                                      ('/scrobble', pages.ScrobblePage),
                                      ('/user/secret', pages.ChangeSecretPage),
                                      ('/user/delete', pages.DeleteUserPage)],
                                     debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
