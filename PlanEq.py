# -*- coding: UTF-8 -*-
import equipment
import workers
from google.appengine.ext import db
from google.appengine.ext import webapp

class PlanEq(db.Model):
	equipment=db.ReferenceProperty(equipment.Equipment)
	quantity=db.IntegerProperty()
	comment=db.StringProperty()
	resp=db.ListProperty(str)
	
class PlanEqPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write(u"""<html><body>
		<a href="..">На главную</a></br>
		<a href="pgplaneqadd">Добавить оборудование в план</a> """)
		peqs=db.GqlQuery('SELECT * FROM PlanEq')
		#db.delete(peqs)
		if peqs.count()==0:
			self.init()
			peqs=db.GqlQuery('SELECT * FROM PlanEq')
	
		self.response.out.write(u"""<table border="1">
														<tr><th>Название</th><th>Колличество</th><th>Комментарий</th><th>Ответственные</th></tr>""")
		for peq in peqs:			
			self.response.out.write(u"<tr> <td>%s<a href=\"/planeq/to-order?kplan=%s\">(Создать заказ)</></td> <td>%s</td><td>%s</td>" % (peq.equipment.name,peq.key(),peq.quantity,peq.comment))
			mstr=str()
			self.response.out.write("<td>")
			for wrkey in peq.resp:
				mstr=mstr+"%s "%db.get(wrkey).surname		
			
			
			
			self.response.out.write("%s</td></tr>" % (mstr))							
		
		self.response.out.write('</table>')
		self.response.out.write(u"""</body></html>""")
		
	def init(self):
		
		pe= PlanEq(equipment=db.get("aghjcnlvbmxhYnIPCxIJRXF1aXBtZW50GAcM"),quantity=1,comment=u'Набор',resp=["aghjcnlvbmxhYnIMCxIGV29ya2VyGAIM"])
		pe.put()
		pe= PlanEq(equipment=db.get("aghjcnlvbmxhYnIPCxIJRXF1aXBtZW50GAgM"),quantity=1,comment=u'Набор',resp =["aghjcnlvbmxhYnIMCxIGV29ya2VyGAMM"])
		pe.put()
		
		pe= PlanEq(equipment=db.get("aghjcnlvbmxhYnIPCxIJRXF1aXBtZW50GAoM"),quantity=1,comment=u'Набор',resp =['aghjcnlvbmxhYnIMCxIGV29ya2VyGAQM','aghjcnlvbmxhYnIMCxIGV29ya2VyGAUM'])
		pe.put()
		
