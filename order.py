# -*-  coding: UTF-8 -*-
import equipment
import vendor
import workers
import payer
import tpay
import lcncss
import verify
import random
import vendor
import payer
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
 			if(unicode(getUsr.key()) in verify.getList([u'Работники',u'Администраторы'])):
				self.doSmf(getUsr)
			elif(unicode(getUsr.key()) in verify.getList([u'Внешние службы'])):
				self.forServ(getUsr)
			else:
				self.redirect('/')
		else:
			self.redirect('/')
		
	def getMyRough(self,caption,wk,stat): # рисует таблицу для заданного пользователя и статуса заявки
		
		rnd_id=random.randrange(20000000)
		
		ords=db.GqlQuery('SELECT * FROM Order WHERE status=:status AND respWk=:respWk',respWk=wk,status=stat)
		
		self.response.out.write(u"""%s(%s)"""%(caption,ords.count()))
		self.response.out.write(u"""<input type="button" id="btn%s" onclick="op_cl('%s')" value="Развернуть">"""%(rnd_id,rnd_id))
		
		self.response.out.write(u"""<div id="%s" style="display:none;">"""%(rnd_id))
		self.response.out.write(u"""<table border="1"><tr><th>Наименование</th><th>Количество</th><th>Цена(руб.)</th><th>Стоимость</th><th>Поставщик</th><th>Дата поставки</th><th>Ответственные</th><th>Одобрено</th></tr>""")
			
		for _ord in ords:
			self.response.out.write(u"<tr>")
			self.response.out.write("<td><a href=\"/order/update-pg?kord=%s\">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(_ord.key(),nameCut(_ord.equipment.name),_ord.quantity,_ord.price,_ord.quantity*_ord.price,_ord.vendor.name,_ord.dateVend,workers.getLnkToProfile(_ord.respWk)))
			ends=db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=_ord)
			self.response.out.write("<td><table>")
			
			for e in ends:
				mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\" DISABLED >"%(e.key())
				if(e.submit==True):
					mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\"CHECKED DISABLED>"%(e.key())
					
				self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"%(workers.getLnkToProfile(e.submiter),mstr))
			
			self.response.out.write("</table></td></tr>")
		self.response.out.write("</table>")
		self.response.out.write("</div>")
		
	def getToSubm(self,caption,sb,subm):
		rnd_id=random.randrange(20000000)
		ends_sb=db.GqlQuery("SELECT * FROM Endorsment WHERE submiter=:submiter AND submit=:submit",submiter=sb,submit=subm)
		
		self.response.out.write(u"""%s(%s)"""%(caption,ends_sb.count()))
		self.response.out.write(u"""<input type="button" id="btn%s" onclick="op_cl('%s')" value="Развернуть">"""%(rnd_id,rnd_id))
		
		self.response.out.write(u"""<div id="%s" style="display:none;">"""%(rnd_id))		
		self.response.out.write(u"""<table border="1"><tr><th>Наименование</th><th>Количество</th><th>Цена(руб.)</th><th>Стоимость</th><th>Поставщик</th><th>Дата поставки</th><th>Ответственные</th><th>Одобрено</th></tr>""")
		
		for _end_sb in ends_sb:
			_ord=_end_sb.order
			if (_ord.status>0):
				self.response.out.write(u"<tr>")
				self.response.out.write("<td><a href=\"/order/update-pg?kord=%s\">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(_ord.key(),nameCut(_ord.equipment.name),_ord.quantity,_ord.price,_ord.quantity*_ord.price,_ord.vendor.name,_ord.dateVend,workers.getLnkToProfile(_ord.respWk)))
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
		self.response.out.write("</table>")
		self.response.out.write("</div>")	
		
	def getRough(self,caption,stat): # рисует таблицу заявок для заданного статуса
		
		rnd_id=random.randrange(20000000)
		
		ords=db.GqlQuery(u'SELECT * FROM Order WHERE status=:status ',status=stat)
		
		self.response.out.write(u"""%s(%s)"""%(caption,ords.count()))
		self.response.out.write(u"""<input type="button" id="btn%s" onclick="op_cl('%s')" value="Развернуть">"""%(rnd_id,rnd_id))
		
		self.response.out.write(u"""<div id="%s" style="display:none;">"""%(rnd_id))
		self.response.out.write(u"""<table border="1"><tr><th>Наименование</th><th>Количество</th><th>Цена(руб.)</th><th>Стоимость</th><th>Поставщик</th><th>Дата поставки</th><th>Ответственные</th><th>Одобрено</th></tr>""")
			
		for _ord in ords:
			self.response.out.write(u"<tr>")
			self.response.out.write("<td><a href=\"/order/update-pg?kord=%s\">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(_ord.key(),nameCut(_ord.equipment.name),_ord.quantity,_ord.price,_ord.quantity*_ord.price,_ord.vendor.name,_ord.dateVend,workers.getLnkToProfile(_ord.respWk)))
			ends=db.GqlQuery("SELECT * FROM Endorsment WHERE order=:order",order=_ord)
			self.response.out.write("<td><table>")
			
			for e in ends:
				mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\" DISABLED >"%(e.key())
				if(e.submit==True):
					mstr="<input type=\"checkbox\" name=\"endsmnt\" value=\"%s\"CHECKED DISABLED>"%(e.key())
					
				self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"%(workers.getLnkToProfile(e.submiter),mstr))
			
			self.response.out.write("</table></td></tr>")
		self.response.out.write("</table>")
		self.response.out.write("</div>")
		
	def getToSubm(self,caption,sb,subm):
		rnd_id=random.randrange(20000000)
		ends_sb=db.GqlQuery("SELECT * FROM Endorsment WHERE submiter=:submiter AND submit=:submit",submiter=sb,submit=subm)
		
		self.response.out.write(u"""%s(%s)"""%(caption,ends_sb.count()))
		self.response.out.write(u"""<input type="button" id="btn%s" onclick="op_cl('%s')" value="Развернуть">"""%(rnd_id,rnd_id))
		
		self.response.out.write(u"""<div id="%s" style="display:none;">"""%(rnd_id))		
		self.response.out.write(u"""<table border="1"><tr><th>Наименование</th><th>Количество</th><th>Цена(руб.)</th><th>Стоимость</th><th>Поставщик</th><th>Дата поставки</th><th>Ответственные</th><th>Одобрено</th></tr>""")
		
		for _end_sb in ends_sb:
			_ord=_end_sb.order
			if (_ord.status>0):
				self.response.out.write(u"<tr>")
				self.response.out.write("<td><a href=\"/order/update-pg?kord=%s\">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(_ord.key(),nameCut(_ord.equipment.name),_ord.quantity,_ord.price,_ord.quantity*_ord.price,_ord.vendor.name,_ord.dateVend,workers.getLnkToProfile(_ord.respWk)))
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
		self.response.out.write("</table>")
		self.response.out.write("</div>")				
################### #############	
	def doSmf(self,cUsr):
		
		self.response.out.write(u"""<html><head>
		<script src="/script/jquery-1.5.2.min.js"></script>
		<script src="/script/jjquery.cookie-modified.js"></script>
		<script type="text/javascript"> 
		$(document).ready(function()
		{
			$("#ord").click(function()
			{ 
				$.cookie({'ord':'myOrd'});
				location.href='/order';
			});				
			$("#subm").click(function()
			{ 
			$.cookie({'ord':'mySbm'});
			location.href='/order';
			});	
			
			$("#allOrd").click(function()
			{ 
			$.cookie({'ord':'allOrd'});
			location.href='/order';
			});					
		
		});
		function op_cl(elid)
		{
			$('#'+elid).toggle(500);
			if($('#btn'+elid)[0].value=='Свернуть')
				$('#btn'+elid)[0].value='Развернуть';
			else if ($('#btn'+elid)[0].value=='Развернуть')
				$('#btn'+elid)[0].value='Свернуть';
		}			
		</script>
		%s</head><body>%s"""%(lcncss.style,lcncss.beg(cUsr.surname)))
			
		#ords=db.GqlQuery('SELECT * FROM Order')
		#ends=db.GqlQuery("SELECT * FROM Endorsment")
		#db.delete(ords)
		#db.delete(ends)
		self.response.out.write(u"""<div class="titlePg">Заявки:</div>""")
		
		self.response.out.write(u""" <input id="ord" type="button" value="Мои заявки"> <input id="subm" type="button" value="На моём одобрении"><input id="allOrd" type="button" value="Все заявки"><br/><br/><div id="tabl">""")
		
		lst_c=self.request.str_cookies
		if ("ord" not in lst_c or (lst_c['ord']=="")):
			self.response.headers.add_header('Set-Cookie',"ord=myOrd; path=/;")
			lst_c['ord']="myOrd"
		
		if(lst_c['ord']=="myOrd"):
			self.response.out.write(u"""<b>Мои заявки</b><br/><br/>""")		
			self.getMyRough(u"""<b>Черновики:</b>""",cUsr,0)		
			self.getMyRough(u"<br/><b>На одобрении:</b>",cUsr,1)		
			self.getMyRough(u"<br/><b>Одобренные:</b>",cUsr,2)	
			self.getMyRough(u"<br/><b>Исполненные:</b>",cUsr,3)	
			
		elif(lst_c['ord']=="mySbm"):
			self.response.out.write(u"<b>На моём одобрении:</b><br/><br/>")		
			self.getToSubm(u"<br/>Одобрить:",cUsr, False)		
			self.getToSubm(u"<br/>Одобренные мной:",cUsr, True)		
		else:
			self.response.out.write(u"""<div class="titlePg">Заявки:</div>""")
			self.getRough(u"<br/><b>Одобренные:</b>",2)		
			self.getRough(u"<br/><b>Исполненные:</b>",3)
						
		self.response.out.write(u"""</div>""")		
		self.response.out.write("%s</body></html>"%lcncss.Mtempl.end)

	
	def forServ(self,cUsr):
		self.response.out.write(u"""<html><head>
		<script src="/script/jquery-1.5.2.min.js"></script>
		<script src="/script/jjquery.cookie-modified.js"></script>
		<script type="text/javascript"> 
		$(document).ready(function()
		{
			$("#ord").click(function()
			{ 
				$.cookie({'ord':'myOrd'});
				location.href='/order';
			});				
			$("#subm").click(function()
			{ 
			$.cookie({'ord':'mySbm'});
			location.href='/order';
			});						
		
		});
		function op_cl(elid)
		{
			$('#'+elid).toggle(500);
			if($('#btn'+elid)[0].value=='Свернуть')
				$('#btn'+elid)[0].value='Развернуть';
			else if ($('#btn'+elid)[0].value=='Развернуть')
				$('#btn'+elid)[0].value='Свернуть';
		}			
		</script>
		%s</head><body>%s"""%(lcncss.style,lcncss.beg(cUsr.surname)))	
		self.response.out.write(u"""<div class="titlePg">Заявки:</div>""")
		self.getRough(u"<br/><b>Одобренные:</b>",2)	
		
		self.getRough(u"<br/><b>Исполненные:</b>",3)
		self.response.out.write(u"%s</body></html>"%lcncss.Mtempl.end)
	
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
		if (self.request.get('vendor')!=''):
			_ord.vendor=db.get(self.request.get('vendor'))
		elif(self.request.get('vdname')!=''):
			vd=vendor.Vendor(name=self.request.get('vdname'))
			vd.put()
			_ord.vendor=vd
		
		_ord.status=int(self.request.get('status'))
		_ord.dateVend=self.request.get('date')
		
		if (self.request.get('payer')!=''):
			_ord.payer=db.get(self.request.get('payer'))
		elif(self.request.get('prname')!=''):
			pr=payer.Payer(name=self.request.get('prname'))
			pr.put()
			_ord.payer=pr
		
		
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
		
def nameCut(name):
	size_str=50
	if len(name)>size_str:
		name=" ".join([name[0:size_str],"..."])
		
	return name
	
