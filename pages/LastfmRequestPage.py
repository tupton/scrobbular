import cgi

from google.appengine.ext import webapp

class LastfmRequestPage(webapp.RequestHandler):
    """A base class for handling requests that interact with Last.fm"""

    def get_params(self):
        """Get the parameters after verifying them"""
        # Required parameters
        required = dict()
        for r in self.required_params:
            required[r] = self.request.get(r).strip()

        for param in self.required_params:
            if not required[param]:
                self.response.set_status(400)
                required_arguments = "\n".join([a + '=' + self.request.get(a) for a in self.required_params])
                optional_arguments = "\n".join([a + '=' + self.request.get(a) for a in self.optional_params])

                self.response.out.write(cgi.escape("Incorrect arguments were supplied:" +
                    "\n\nRequired:\n" + required_arguments + "\n\nOptional:\n" + optional_arguments))
                return None

        # Optional parameters
        optional = dict()
        for o in self.optional_params:
            optional[o] = self.request.get(o).strip()

        params = required
        params.update(optional)

        return params
        
