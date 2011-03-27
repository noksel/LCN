#-*- coding: UTF-8 -*-
import equipment
import vendor
import workers
from google.appengine.ext import db
from google.appengine.ext import webapp

class Order(db.Model):
	equipment=db.ReferenceProperty(equipment.Equipment)
	quantity=db.IntegerProperty()
	price=db.IntegerProperty()
	vendor=db.ReferenceProperty(vendor.Vendor)
	status=db.IntegerProperty()
	dateVend=db.StringProperty()
	typePayment=db.StringProperty() 
	tz=db.StringProperty(multiline=True)
	resp=db.ListProperty(str)
	
class Endorsment(db.Model):
	order=db.ReferenceProperty(Order)
	worker=db.ReferenceProperty(workers.Worker)
	submit=db.BooleanProperty()
	comment=db.StringProperty()
	
	
class OrderPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write("""
		<html><body>
			""")
			
		ords=db.GqlQuery('SELECT * FROM Order')
		#db.delete(ords)
		
		if(ords.count()==0):
			self.init()
			ords=db.GqlQuery('SELECT * FROM Order')
		self.response.out.write(u"""<form metond="GET" action="/asdas"><table border="1"><tr><th>Наименование</th><th>Количество</th><th>Цена</th><th>Стоимость</th><th>Тип оплаты</th><th>Ответственные</th><th>Статус</th><th>Одобрено</th></tr>""")
		
	
		for _ord in ords:
			mstr=str()
			for swk in _ord.resp:
				mstr=mstr+" %s"%db.get(swk).surname
			if(_ord.status==0):
				st=u'Черновик'
			self.response.out.write("<tr>")
			self.response.out.write("<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(_ord.equipment.name,_ord.quantity,_ord.price,_ord.quantity*_ord.price,_ord.typePayment,mstr,st))
			ends=db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=_ord)
			self.response.out.write("<td><table>")
			
			for e in ends:
				mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\" onclick=\"javascript:window.location.href='/order/submit?endsmnt=%s'\">"%(e.key(),e.key())
				if(e.submit==True):
					mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\"CHECKED DISABLED>"%(e.key())
					
				self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"%(e.worker.surname,mstr))
			
			self.response.out.write("</table></td></tr>")
		self.response.out.write('</table></form></body></html>')
	
	def init(self):
		ordr=Order(equipment=db.get("aghjcnlvbmxhYnIPCxIJRXF1aXBtZW50GAsM"),quantity=1,price=19000,vendor=db.get("aghjcnlvbmxhYnIMCxIGVmVuZG9yGBEM"),status=0,typePayment=u'счёт',tz="",resp=[u'aghjcnlvbmxhYnIMCxIGV29ya2VyGAIM'])
		ordr.put()
		
		ends=Endorsment(order=ordr,worker=db.get('aghjcnlvbmxhYnIMCxIGV29ya2VyGAYM'),submit=False)
		ends.put()
		
		ends=Endorsment(order=ordr,worker=db.get('aghjcnlvbmxhYnIMCxIGV29ya2VyGAUM'),submit=True)
		ends.put()

