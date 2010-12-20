from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import pages

application = webapp.WSGIApplication(
                                     [('/', pages.IndexPage),
                                      ('/submit', pages.SubmitPage),
                                      ('/user.*', pages.UserPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
