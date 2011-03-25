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
		
		
		if(ords.count()==0):
			self.init()
			ords=db.GqlQuery('SELECT * FROM Order')
		self.response.out.write('<table border="1">')
		mstr=str()
	
		for _ord in ords:
			for swk in _ord.resp:
				mstr=mstr+" %s"%db.get(swk).surname
			self.response.out.write("<tr>")
			self.response.out.write("<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(_ord.equipment.name,_ord.quantity,_ord.price,_ord.typePayment,mstr,_ord.key()))
			ends=db.GqlQuery("SELECT * FROM Endorsment")
			db.delete(ends)
			self.init()
			ends=db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=_ord)
			self.response.out.write("<td><table>")
			for e in ends:
				mstr="<input type=\"checkbox\" name=\"subm\" value=\"%s\">"%e.key()
				if(e.submit==True):
					mstr="<input type=\"checkbox\" name=\"subm\" value=\"%s\" CHECKED DISABLED>"%e.key()
					
				self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"%(e.worker.surname,mstr))
			
			self.response.out.write("</table></td></tr>")
		self.response.out.write('</table></body></html>')
	
	def init(self):
		#order=Order(equipment=db.get("aghjcnlvbmxhYnIPCxIJRXF1aXBtZW50GBoM"),quantity=1,price=19000,vendor=db.get("aghjcnlvbmxhYnIMCxIGVmVuZG9yGBEM"),status=0,typePayment=u'счёт',tz="",resp=[u'aghjcnlvbmxhYnIMCxIGV29ya2VyGAIM'])
	#	order.put()
		
		ends=Endorsment(order=db.get('aghjcnlvbmxhYnILCxIFT3JkZXIYTww'),worker=db.get('aghjcnlvbmxhYnIMCxIGV29ya2VyGAYM'),submit=False)
		ends.put()
		
		ends=Endorsment(order=db.get('aghjcnlvbmxhYnILCxIFT3JkZXIYTww'),worker=db.get('aghjcnlvbmxhYnIMCxIGV29ya2VyGAUM'),submit=True)
		ends.put()

