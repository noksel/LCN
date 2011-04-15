#-*- coding: UTF-8 -*-

import order
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp
#подумать. идёт номер заказа а одобряющего берём из куков.
class submEnd(webapp.RequestHandler):
	def get(self):
		endrsmnt=db.get(self.request.get('endsmnt'))
		getUsr=verify.verifyUsr(self)
		
		if (verify.verifyRightEndors(getUsr,endrsmnt)):
			self.doSmf()
		else:
			self.redirect('/order')
					
	def doSmf(self):
		
		endrsmnt=db.get(self.request.get('endsmnt'))
		if (endrsmnt.order.status==1):
			endrsmnt.submit=True
			endrsmnt.put()
			ends=db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=endrsmnt.order)
			allsb=True
			for end in ends:
				if (end.submit==False):
					allsb=False
					
			if(allsb==True):
				_ord=endrsmnt.order
				_ord.status=2
				_ord.put()
				
		self.redirect('/order')
		
