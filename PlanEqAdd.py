#-*- coding: UTF-8 -*-

import workers
import equipment
import PlanEq

from google.appengine.ext import db
from google.appengine.ext import webapp
class PEAdd(webapp.RequestHandler):
	def get(self):
		pe=PlanEq.PlanEq()
		
		pe.idEquipment=db.get(self.request.get('eqid'))
		pe.quantity=int(self.request.get('quant'))
		pe.comment=self.request.get('comment')
		self.response.out.write("%s _ %s _ %s"%(pe.idEquipment.name,pe.quantity,pe.comment))
		#self.response.out.write("%s _ %s _ "%(pe.quantity,pe.comment))
		#pe.resp=[self.request.get('resp')]
		#self.response.out.write(self.request.get('resp').split(':'))
		#pe.put()
