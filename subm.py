#-*- coding: UTF-8 -*-

import order
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp
#подумать. идёт номер заказа а одобряющего берём из куков.
class submEnd(webapp.RequestHandler):
	def get(self):
		endrsmnt=db.get(self.request.get('endsmnt'))
		
		if (verify.verifyRightEndors(self,endrsmnt)):
			self.doSmf()
		else:
			pass
			self.redirect('/order')
					
	def doSmf(self):
		endrsmnt=db.get(self.request.get('endsmnt'))
		endrsmnt.submit=True
		endrsmnt.put()
		self.redirect('/order')
		
