#-*- coding: UTF-8 -*-
import workers
import verify
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Notice(db.Model):
	title=db.StringProperty()
	body=db.TextProperty()
	author=db.ReferenceProperty(workers.Worker)
	date = db.DateTimeProperty(auto_now_add=True)
	
class AddNotice(webapp.RequestHandler):
	def post(self):
		cUsr=verify.verifyUsr(self)
 		if (cUsr!=None):
			if(unicode(cUsr.key()) in verify.getList([u'Администраторы',u'Работники',u'Внешние службы'])):
				self.doSmf(cUsr)			
		else:
			self.redirect('/')
	
	def doSmf(self,cUsr):
		nt=Notice()
		
		nt.author=cUsr
		nt.title=self.request.get('title')
		nt.body=self.request.get('body')
		nt.put()
		self.redirect('/')
