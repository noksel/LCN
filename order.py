#-*- coding: UTF-8 -*-
import equipment
import vendor
import workers
import payer
import tpay
import lcncss
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class Order(db.Model):
	equipment=db.ReferenceProperty(equipment.Equipment)
	quantity=db.IntegerProperty()
	price=db.FloatProperty()
	vendor=db.ReferenceProperty(vendor.Vendor)
	status=db.IntegerProperty()
	dateVend=db.StringProperty()
	payer=db.ReferenceProperty(payer.Payer)
	typePayment=db.ReferenceProperty(tpay.TypePayment)
	tz=db.StringProperty(multiline=True)
	resp=db.ListProperty(str)
	
class Endorsment(db.Model):
	order=db.ReferenceProperty(Order)
	submiter=db.ReferenceProperty(workers.Worker)
	submit=db.BooleanProperty()
	comment=db.StringProperty()
	
	
class OrderPage(webapp.RequestHandler):
	def get(self):
			if (verify.verifyUsr(self)):
				self.doSmf()
			else:
				self.redirect('/')
	
	def doSmf(self):
		wk= db.get(self.request.str_cookies['session'])
		self.response.out.write("""<html><head>%s</head><body>%s"""%(lcncss.style,lcncss.beg(wk.surname)))
			
		ords=db.GqlQuery('SELECT * FROM Order')
		ends=db.GqlQuery("SELECT * FROM Endorsment")
		#db.delete(ords)
		#db.delete(ends)
		
		self.response.out.write(u"""<table border="1"><tr><th>Наименование</th><th>Количество</th><th>Цена</th><th>Стоимость</th><th>Поставщик</th><th>Дата поставки</th><th>Ответственные</th><th>Статус</th><th>Одобрено</th></tr>""")
		
	
		for _ord in ords:
			mstr=str()
			mstr=" ".join([db.get(wrkey).surname for wrkey in _ord.resp])	
				
			if(_ord.status==0):
				st=u'Черновик'
			elif (_ord.status==1):
				st=u'На одобрение'
			elif (_ord.status==2):
				st=u'Выполнено'
			self.response.out.write("<tr>")
			self.response.out.write("<td><a href=\"/order/update-pg?kord=%s\">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(_ord.key(),_ord.equipment.name,_ord.quantity,_ord.price,_ord.quantity*_ord.price,_ord.vendor.name,_ord.dateVend,mstr,st))
			ends=db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=_ord)
			self.response.out.write("<td><table>")
			
			for e in ends:
				mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\" onclick=\"javascript:window.location.href='/order/submit?endsmnt=%s'\">"%(e.key(),e.key())
				if(e.submit==True):
					mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\"CHECKED DISABLED>"%(e.key())
					
				self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"%(e.submiter.surname,mstr))
			
			self.response.out.write("</table></td></tr>")
		self.response.out.write("</table>%s</body></html>"%lcncss.Mtempl.end)
	
class OrdAdd(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
	def doSmf(self):	
		_ord=Order()
		_ord.equipment=db.get(self.request.get('eqipm'))
		_ord.quantity=int(self.request.get('quant'))
		_ord.price=float(self.request.get('price'))
		_ord.vendor=db.get(self.request.get('vendor'))
		_ord.status=int(self.request.get('status'))
		_ord.dateVend=self.request.get('date')
		_ord.payer=db.get(self.request.get('payer'))
		_ord.typePayment=db.get(self.request.get('tpay'))	
		_ord.tz=self.request.get('tz')
		_ord.resp=self.request.get('resp').split(':')
		_ord.put()

		
		
		
		wks=self.request.get('ends').split(':')
		for wk in wks:
			_end=Endorsment()
			_end.order=_ord
			_end.submiter=db.get(wk)
			_end.submit=False
			_end.comment=""
			_end.put()			
		self.redirect('/order')
class OrdUpdate(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
	
	def doSmf(self):
		_ord=db.get(self.request.get('ord'))
		_ord.quantity=int(self.request.get('quant'))
		_ord.price=float(self.request.get('price'))
		_ord.vendor=db.get(self.request.get('vendor'))
		_ord.status=int(self.request.get('status'))
		_ord.dateVend=self.request.get('date')
		_ord.payer=db.get(self.request.get('payer'))
		_ord.typePayment=db.get(self.request.get('tpay'))	
		_ord.tz=self.request.get('tz')
		_ord.resp=self.request.get('resp').split(':')
		_ord.put()

				
		ends= db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=_ord)
		db.delete(ends)
		wks=self.request.get('ends').split(':')
		for wk in wks:
			_end=Endorsment()
			_end.order=_ord
			_end.submiter=db.get(wk)
			_end.submit=False
			_end.comment=""
			_end.put()			
		self.redirect('/order')
