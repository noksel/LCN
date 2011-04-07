#-*- coding: UTF-8 -*-

import order
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp
#подумать. идёт номер заказа а одобряющего берём из куков.
class submEnd(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
					
	def doSmf(self):
		endsmnt=db.get(self.request.get('endsmnt'))
		endsmnt.submit=True
		endsmnt.put()
		self.redirect('/order')
		
