import workers
from google.appengine.ext import db
from google.appengine.ext import webapp

class AddWorker(webapp.RequestHandler):
	def post(self):
		wk=workers.Worker()
		wk.surname=self.request.get('surname')
		wk.name=self.request.get('name')
		wk.email=self.request.get('email')
		wk.phone=self.request.get('phone')
		wk.put()
		self.redirect('/workers')
