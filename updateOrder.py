# -*-  coding: UTF-8 -*-
import lcncss
import my_js
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class UpdateOrderPg(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')	
	def doSmf(self):
		_ord=db.get(self.request.get('kord'))
		wk= db.get(self.request.str_cookies['session'])
		self.response.out.write(u"""<html><head>%s<script>equipment='%s';	%s
		</script></head><body>%s<b>Правка заявки</b><table>"""%(lcncss.style,_ord.equipment.key(), my_js.getChList,lcncss.beg(wk.surname)))
		
		self.response.out.write(u"<tr><td>Оборудование: </td><td>%s</td></tr>"%_ord.equipment.name)
		self.response.out.write(u"<tr><td>Количество:</td> <td><input id=\"quant\" value=\"%s\"></td></tr>"%_ord.quantity)
		
		self.response.out.write(u"<tr><td>Цена:</td> <td><input name=\"price\" value=\"%s\"></td></tr>"%_ord.price)

		self.response.out.write(u"<tr><td>Поставщик:</td> <td><SELECT name=\"vendor\">")
		vds =db.GqlQuery("SELECT * FROM Vendor")
		
		for vd in vds:
			if(vd.key()==_ord.vendor.key()):
				self.response.out.write(u"<OPTION SELECTED value=\"%s\">%s\n"%(vd.key(),vd.name))
			else:
				self.response.out.write(u"<OPTION value=\"%s\">%s"%(vd.key(),vd.name))
			
		self.response.out.write(u"</SELECT></td></tr>")
		self.response.out.write(u"""<tr><td>Статус заявки:</td> <td><SELECT name=\"status\">""")
		
		if(_ord.status==0):
			self.response.out.write(u"""<OPTION SELECTED value=\"0\">Черновик
																<OPTION value=\"1\">На одобрение</SELECT></td></tr>""")
		elif (_ord.status==1):
			self.response.out.write(u"""
				<OPTION value=\"0\">Черновик
				<OPTION SELECTED value=\"1\">На одобрение</SELECT></td></tr>""")
		elif (_ord.status==2):
			self.response.out.write(u"""
				<OPTION value=\"0\">Черновик
				<OPTION SELECTED value=\"2\">Одобрена</SELECT></td></tr>""")		
				
		self.response.out.write(u"""<tr><td>Дата поставки:</td> <td><input name=\"dateVend\" value=\"%s\"></td></tr>"""%_ord.dateVend)
		
		self.response.out.write(u"<tr><td>Плательщик:</td> <td><SELECT name=\"payer\">")
		prs =db.GqlQuery("SELECT * FROM Payer")		
		for pr in prs:
			if(pr.key()==_ord.payer.key()):
				self.response.out.write(u"<OPTION SELECTED value=\"%s\">%s"%(pr.key(),pr.name))			
			else:
				self.response.out.write(u"<OPTION value=\"%s\">%s"%(pr.key(),pr.name))			
		
		self.response.out.write(u"</SELECT></td></tr>")
		
		self.response.out.write(u"""<tr><td>Тип оплаты:</td><td><SELECT name="tpaymnt">""")
		tps=db.GqlQuery("SELECT * FROM TypePayment")
		
		for tp in tps:
			if(tp.key()==_ord.typePayment.key()):
				self.response.out.write(u"<OPTION SELECTED value=\"%s\">%s"%(tp.key(),tp.name))
			else:
				self.response.out.write(u"<OPTION value=\"%s\">%s"%(tp.key(),tp.name))	
		self.response.out.write(u"""</SELECT></td></tr>		
				<tr><td>Тех.здание:</td> <td><textarea name="tz" rows="5" cols="40" >%s</textarea></td></tr>"""%_ord.tz) #опциональное
				
		self.response.out.write(u"<tr><td>Ответственные:</td> <td>%s</td></tr></table>"%_ord.respWk.surname)
		
		self.response.out.write(u'Утверждают:</br>')
	
	
		wks=db.GqlQuery('SELECT * FROM Worker ORDER BY surname')
		ends=db.GqlQuery('SELECT * FROM Endorsment WHERE order=:order',order=_ord)
	
		
		
		for wk in wks:
			tmp=False
			for end in ends:
				if (wk.key()==end.submiter.key()):
					tmp=True
					break
			if(tmp==True):
				if(wk.key()!=_ord.respWk.key()):
					self.response.out.write(u"<input CHECKED type=\"checkbox\" name=\"submiters\" value=\"%s\">%s</br>"%(wk.key(),wk.surname))		
			else:
				if(wk.key()!=_ord.respWk.key()):
					self.response.out.write(u"<input type=\"checkbox\" name=\"submiters\" value=\"%s\">%s</br>"%(wk.key(),wk.surname))
					
		# количество обновляется. вернуть в план??
		self.response.out.write(u"""<input type="button" value="Принять" onclick="javascript:window.location.href='/order/update?ord=%s'+'&quant='+document.getElementById('quant').value+'&price='+document.getElementsByName('price')[0].value+'&vendor='+document.getElementsByName('vendor')[0].value+'&status='+document.getElementsByName('status')[0].value+'&date='+document.getElementsByName('dateVend')[0].value+'&payer='+document.getElementsByName('payer')[0].value+'&tpay='+document.getElementsByName('tpaymnt')[0].value+'&tz='+document.getElementsByName('tz')[0].value+'&resp=%s'+'&ends='+getList('submiters')">%s</body></html>"""%(_ord.key(),_ord.respWk.key(),lcncss.Mtempl.end))
