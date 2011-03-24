# -*- coding: UTF-8 -*-

import cgi
import workers
import wadd
import equipment
import wsgiref.handlers
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
	self.response.out.write(u"""
		<html>
		<body>
			<a href="workers">Сотрудники</a></br>
			<a href="equipment">Оборудование</a>
		</body>
		</html>

		""")
appl = webapp.WSGIApplication([('/', MainPage)
															,('/workers',workers.WorkersPage)
															,('/workers/add',wadd.AddWorker)
															,('/equipment',equipment.EqPage)],debug=True)

def main():
 wsgiref.handlers.CGIHandler().run(appl)
 
if __name__=="__main__":
	main()
