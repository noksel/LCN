import workers
import verify
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Notice(db.Model):
	title=db.StringProperty()
	body=db.StringProperty(multiline=True)
	author=db.ReferenceProperty(workers.Worker)
	date = db.DateTimeProperty(auto_now_add=True)
	
class AddNotice(webapp.RequestHandler):
	def post(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')	
	
	def doSmf(self):
		nt=Notice()
		wk= db.get(self.request.str_cookies['session'])
		nt.author=wk
		nt.title=self.request.get('title')
		nt.body=self.request.get('body')
		nt.put()
		self.redirect('/')
