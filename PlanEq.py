# -*- coding: UTF-8 -*-

import equipment
import workers
from google.appengine.ext import db
from google.appengine.ext import webapp

class PlanEq(db.Model):
	idEquipment=db.ReferenceProperty(equipment.Equipment)
	quantity=db.IntegerProperty()
	comment=db.StringProperty()
	resp=db.ListProperty(unicode)
	
class PlanEqPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write("""<html><body>""")
		peqs=db.GqlQuery('SELECT * FROM PlanEq')
		#db.delete(peqs)
		if peqs.count()==0:
			self.init()
			peqs=db.GqlQuery('SELECT * FROM PlanEq')
	
		self.response.out.write(u"""<table border="1">
														<tr><th>Название</th><th>Колличество</th><th>Комментарий</th><th>Ответственные</th></tr>""")
		for peq in peqs:			
			self.response.out.write("<tr> <td>%s</td> <td>%s</td><td>%s</td>" % (peq.idEquipment.name,peq.quantity,peq.comment))
			mstr=unicode()
			self.response.out.write("<td>")
			for wrkey in peq.resp:
				mstr=mstr+"%s "%db.get(wrkey).surname		
			
			
			
		self.response.out.write("%s</td></tr>" % mstr)							
		
		self.response.out.write('</table>')
		self.response.out.write("""</body></html>""")
		
	def init(self):
		
		pe= PlanEq(idEquipment=db.get("aghjcnlvbmxhYnIPCxIJRXF1aXBtZW50GAkM"),quantity=1,comment=u'Набор',resp=['aghjcnlvbmxhYnIMCxIGV29ya2VyGEQM'])
		pe.put()
		pe= PlanEq(idEquipment=db.get("aghjcnlvbmxhYnIPCxIJRXF1aXBtZW50GAoM"),quantity=1,comment=u'Набор',resp =['aghjcnlvbmxhYnIMCxIGV29ya2VyGEUM'])
		pe.put()
		
		pe= PlanEq(idEquipment=db.get("aghjcnlvbmxhYnIPCxIJRXF1aXBtZW50GAwM"),quantity=1,comment=u'Набор',resp =['aghjcnlvbmxhYnIMCxIGV29ya2VyGEYM',u'aghjcnlvbmxhYnIMCxIGV29ya2VyGEcM'])
		pe.put()
		
