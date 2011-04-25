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
	status=db.IntegerProperty() # 0-черновик, 1-на одобрении, 2-одобрен, 3-исполнен.
	dateVend=db.StringProperty()
	payer=db.ReferenceProperty(payer.Payer)
	typePayment=db.ReferenceProperty(tpay.TypePayment)
	tz=db.StringProperty()
	respWk=db.ReferenceProperty(workers.Worker)
	dateUpd = db.DateTimeProperty(auto_now=True)
	
class Endorsment(db.Model):
	order=db.ReferenceProperty(Order)
	submiter=db.ReferenceProperty(workers.Worker)
	submit=db.BooleanProperty()
	comment=db.StringProperty()
	
class OrderPage(webapp.RequestHandler):
	def get(self):
		getUsr=verify.verifyUsr(self)
 		if (getUsr!=None):
			self.doSmf(getUsr)			
		else:
			self.redirect('/')
		
	def getMyRough(self,wk,stat):
		
		ords=db.GqlQuery('SELECT * FROM Order WHERE status=:status AND respWk=:respWk',respWk=wk,status=stat)
			
		for _ord in ords:
			self.response.out.write(u"<tr>")
			self.response.out.write("<td><a href=\"/order/update-pg?kord=%s\">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(_ord.key(),_ord.equipment.name,_ord.quantity,_ord.price,_ord.quantity*_ord.price,_ord.vendor.name,_ord.dateVend,workers.getLnkToProfile(_ord.respWk)))
			ends=db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=_ord)
			self.response.out.write("<td><table>")
			
			for e in ends:
				mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\" DISABLED >"%(e.key())
				if(e.submit==True):
					mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\"CHECKED DISABLED>"%(e.key())
					
				self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"%(workers.getLnkToProfile(e.submiter),mstr))
			
			self.response.out.write("</table></td></tr>")
		
	def getToSubm(self,sb,subm):
		ends_sb=db.GqlQuery("SELECT * FROM Endorsment WHERE submiter=:submiter AND submit=:submit",submiter=sb,submit=subm)
		
		for _end_sb in ends_sb:
			_ord=_end_sb.order
			if (_ord.status==1 or _ord.status==2):
				self.response.out.write(u"<tr>")
				self.response.out.write("<td><a href=\"/order/update-pg?kord=%s\">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(_ord.key(),_ord.equipment.name,_ord.quantity,_ord.price,_ord.quantity*_ord.price,_ord.vendor.name,_ord.dateVend,workers.getLnkToProfile(_ord.respWk)))
				ends=db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=_ord)
				self.response.out.write("<td><table>")
			
				for e in ends:
					mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\" onclick=\"javascript:window.location.href=\\\'/order/submit?endsmnt=%s\\\'\">"%(str(e.key()),str(e.key()))
					if(e.submit==True):
						mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\"CHECKED DISABLED>"%(e.key())
					elif(sb.key()!=e.submiter.key()):
						mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\"DISABLED>"%(e.key())
						
					self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"%(workers.getLnkToProfile(e.submiter),mstr))
			
				self.response.out.write("</table></td></tr>")		
################### #############	
	def doSmf(self,cUsr):
		
		self.response.out.write("""<html><head>
		<script src="/script/jquery-1.5.2.min.js"></script>
		<script type="text/javascript"> 
		$(document).ready(function()
		{
			$("#ord").click(function()
			{ $("#tabl").replaceWith('""")
			
		self.response.out.write(u"""<div id="tabl"> """)
		self.response.out.write(u"""<b>Мои заявки</b><br/><table border="1"><tr><th>Наименование</th><th>Количество</th><th>Цена(руб.)</th><th>Стоимость</th><th>Поставщик</th><th>Дата поставки</th><th>Ответственные</th><th>Одобрено</th></tr><tr><td>Черновики</td></tr>""")
		self.getMyRough(cUsr,0)
		self.response.out.write(u"<tr><td>На одобрении:</td></tr>")
		self.getMyRough(cUsr,1)
		
		self.response.out.write(u"<tr><td>Одобренные:</td></tr>")
		self.getMyRough(cUsr,2)		
		self.response.out.write(u"<tr><td>Исполненные:</td></tr>")
		self.getMyRough(cUsr,3)	
		self.response.out.write("</table> </div>');")
					
			
		self.response.out.write("""	
			});				
			$("#subm").click(function()
			{ $("#tabl").replaceWith('	""")
		
		self.response.out.write(u"""<div id="tabl"> """)	
		self.response.out.write(u"""<b>На моём одобрении:</b><br/><table border="1"><tr><th>Наименование</th><th>Количество</th><th>Цена(руб.)</th><th>Стоимость</th><th>Поставщик</th><th>Дата поставки</th><th>Ответственные</th><th>Одобрено</th></tr>""")
		
		self.response.out.write(u"<tr><td>Одобрить:</td></tr>")
		self.getToSubm(cUsr, False)
		self.response.out.write(u"<tr><td>Одобренные мной:</td></tr>")
		self.getToSubm(cUsr, True)				
		
		self.response.out.write("</table></div>');")	
				
		self.response.out.write("""	});		
		$("#ord").click();
		});	
		</script>
		%s</head><body>%s"""%(lcncss.style,lcncss.beg(cUsr.surname)))
			
		#ords=db.GqlQuery('SELECT * FROM Order')
		#ends=db.GqlQuery("SELECT * FROM Endorsment")
		#db.delete(ords)
		#db.delete(ends)
		self.response.out.write(u"""<div class="titlePg">Заявки:</div>""")
		
		self.response.out.write(u""" <input id="ord" type="button" value="Мои заявки"> <input id="subm" type="button" value="На моём одобрении"><br/><br/><div id="tabl"></div>""")
		
		self.response.out.write("%s</body></html>"%lcncss.Mtempl.end)
	
class OrdAdd(webapp.RequestHandler):
	def get(self):
		cUsr=verify.verifyUsr(self)
 		if (cUsr!=None):
			if(unicode(cUsr.key()) in verify.getList([u'Администраторы',u'Работники'])):
				self.doSmf()			
		else:
			self.redirect('/')
	def doSmf(self):	
		_ord=Order()
		_ord.equipment=db.get(self.request.get('eqipm'))
		try:
			_ord.quantity=int(self.request.get('quant'))
		except(ValueError):
			_ord.quantity=0
	
		try:
			_ord.price=float(self.request.get('price').replace(',','.'))
		except(ValueError):
			_ord.price=0.0
			
		_ord.vendor=db.get(self.request.get('vendor'))
		_ord.status=int(self.request.get('status'))
		_ord.dateVend=self.request.get('date')
		_ord.payer=db.get(self.request.get('payer'))
		_ord.typePayment=db.get(self.request.get('tpay'))	
		_ord.tz=self.request.get('tz')
		_ord.respWk=db.get(self.request.get('resp'))
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
		cUsr=verify.verifyUsr(self)
 		if (cUsr!=None):
			self.doSmf(cUsr)			
		else:
			self.redirect('/')
	
	def doSmf(self,cUsr):
		_ord=db.get(self.request.get('ord'))
		
		if(cUsr.key()==_ord.respWk.key()):
		
			_ord.quantity=int(self.request.get('quant'))
			_ord.price=float(self.request.get('price').replace(',','.'))
			_ord.vendor=db.get(self.request.get('vendor'))
			_ord.status=int(self.request.get('status'))
			_ord.dateVend=self.request.get('date')
			_ord.payer=db.get(self.request.get('payer'))
			_ord.typePayment=db.get(self.request.get('tpay'))	
			_ord.tz=self.request.get('tz')
			_ord.respWk=db.get(self.request.get('resp'))
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
		
class OrdToHist(webapp.RequestHandler):
	def get(self):
		cUsr=verify.verifyUsr(self)
 		if (cUsr!=None):
			self.doSmf(cUsr)			
		else:
			self.redirect('/')
			
	def doSmf(self,cUsr):	
		_ord=db.get(self.request.get('ord'))
		if(cUsr.key()==_ord.respWk.key()):
			_ord.status=3 
			_ord.put()
		self.redirect('/order')	
		
class DellOrd(webapp.RequestHandler):
	def get(self):
		cUsr=verify.verifyUsr(self)
 		if (cUsr!=None):
			self.doSmf(cUsr)			
		else:
			self.redirect('/')
			
	def doSmf(self,cUsr):	
		_ord=db.get(self.request.get('ord'))
		if(cUsr.key()==_ord.respWk.key()):
			ends= db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=_ord)
			db.delete(ends)
			db.delete(_ord)
		self.redirect('/order')
