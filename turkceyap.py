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

        # self.response.out.write('<html><body>')
        # submitted_contents = db.GqlQuery("SELECT * FROM SubmittedContent ORDER BY date DESC LIMIT 10")
        # for submitted_content in submitted_contents:
        #     if submitted_content.author:
        #         self.response.out.write('<b>%s</b> wrote:' % submitted_content.author.nickname())
        #     else:
        #         self.response.out.write('An anonymous person wrote:')
        #     self.response.out.write('<blockquote>%s</blockquote>' %
        #                             cgi.escape(submitted_content.content))
        # self.response.out.write("""
        #       <form action="/deasciify" method="post">
        #         <div><textarea name="content" rows="3" cols="60"></textarea></div>
        #         <div><input type="submit" value="deasciify"></div>
        #       </form>
        #     </body>
        #   </html>""")


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

        #self.response.out.write('<html><body>You wrote:<pre>')
        #self.response.out.write(cgi.escape(result))
        #self.response.out.write('</pre></body></html>')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/deasciify', GaeDeasciifier)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

