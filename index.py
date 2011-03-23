import cgi
import workers
import wsgiref.handlers
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
	self.response.out.write("""
		<html>
		<body>
			<a href="workers">wrk</a>
		</body>
		</html>

		""")
appl = webapp.WSGIApplication([('/', MainPage),('/workers',workers.WorkersPage)],debug=True)

def main():
 wsgiref.handlers.CGIHandler().run(appl)
 
if __name__=="__main__":
	main()
