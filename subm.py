#-*- coding: UTF-8 -*-

import order

from google.appengine.ext import db
from google.appengine.ext import webapp

class submEnd(webapp.RequestHandler):
	def get(self):
		endsmnt=db.get(self.request.get('endsmnt'))
		endsmnt.submit=True
		endsmnt.put()
		self.redirect('/order')
		
