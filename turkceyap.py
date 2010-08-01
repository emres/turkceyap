import cgi
import os

from turkish.deasciifier import Deasciifier 

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class SubmittedContent(db.Model):
    author = db.UserProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    """
    """
    def get(self):
        user = users.get_current_user()        
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class GaeDeasciifier(webapp.RequestHandler):
    """
    """
    def post(self):

        submitted_content = SubmittedContent()

        if users.get_current_user():
            submitted_content.author = users.get_current_user()

        submitted_content.content = self.request.get('content')
        
        submitted_content.put()      

        string = cgi.escape(self.request.get('content'))
        dea = Deasciifier(string)
        result = dea.convert_to_turkish()
        
        template_values = {'result': result}

        path = os.path.join(os.path.dirname(__file__), 'deasciify.html')
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/deasciify', GaeDeasciifier)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
