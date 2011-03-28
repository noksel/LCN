# -*- coding UTF-8 -*-
import order

from google.appengine.ext import db
from google.appengine.ext import webapp

class Ordadd(webapp.RequestHandler):
	def get(self):
		_ord=order.Order()
		_ord.equipment=db.get(self.request.get('eqipm'))
		_ord.quantity=int(self.request.get('quant'))
		_ord.price=int(self.request.get('price'))
		_ord.vendor=db.get(self.request.get('vendor'))
		_ord.status=int(self.request.get('status'))
		_ord.dateVend=self.request.get('date')
		_ord.typePament=self.request.get('tpay')
		_ord.resp=self.request.get('resp').split(':')
		_ord.put()

		
		
		
		wks=self.request.get('ends').split(':')
		for wk in wks:
			_end=order.Endorsment()
			_end.order=_ord
			_end.worker=db.get(wk)
			_end.submit=False
			_end.comment=""
			_end.put()
			
		self.redirect('/order')
