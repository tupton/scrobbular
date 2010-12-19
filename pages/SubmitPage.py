import cgi

from google.appengine.ext import webapp

class SubmitPage(webapp.RequestHandler):
    def post(self):
        self.response.out.write(cgi.escape("\n".join([a + '=' + self.request.get(a) for a in self.request.arguments()])))

    def get(self):
        self.response.out.write('submit!')

