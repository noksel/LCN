# -*-  coding: UTF-8 -*-
import lcncss
import my_js
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class ToOrderPage(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
				
	def doSmf(self):
		pl=db.get(self.request.get('kplan'))
		wk= db.get(self.request.str_cookies['session'])
		self.response.out.write(u"""<html><head>%s<script src="/script/my.js"></script><script>equipment='%s';</script>
			</head><body>%s <b>Создание заявки</b><table>"""%(lcncss.style,pl.equipment.key(),lcncss.beg(wk.surname)))
		self.response.out.write(u"<tr><td>Оборудование: </td><td>%s</td></tr>"%pl.equipment.name)
		self.response.out.write(u"<tr><td>Количество:</td> <td><input id=\"quant\" value=\"%s\"></td></tr>"%pl.quantity)
		
		self.response.out.write(u"<tr><td>Цена:</td> <td><input name=\"price\"></td></tr>")

		self.response.out.write(u"<tr><td>Поставщик:</td> <td><SELECT name=\"vendor\">")
		vds =db.GqlQuery("SELECT * FROM Vendor")
		
		for vd in vds:
			self.response.out.write(u"<OPTION value=\"%s\">%s"%(vd.key(),vd.name))
			
		self.response.out.write(u"</SELECT></td></tr>")
		self.response.out.write(u"""<tr><td>Статус заявки:</td> <td><SELECT name=\"status\">
				<OPTION value=\"0\">Черновик
				<OPTION value=\"1\">На одобрение</SELECT></td></tr>
				<tr><td>Дата поставки:</td> <td><input name=\"dateVend\"></td></tr>""")
				
		
		self.response.out.write(u"<tr><td>Плательщик:</td> <td><SELECT name=\"payer\">")
		prs =db.GqlQuery("SELECT * FROM Payer")
		
		for pr in prs:
			self.response.out.write(u"<OPTION value=\"%s\">%s"%(pr.key(),pr.name))
			
		self.response.out.write(u"</SELECT></td></tr>")	
				
				
		self.response.out.write(u"""<tr><td>Тип оплаты:</td><td><SELECT name="tpaymnt">""")
		tps=db.GqlQuery("SELECT * FROM TypePayment")
		for tp in tps:
			self.response.out.write(u"<OPTION value=\"%s\">%s"%(tp.key(),tp.name))
		
		self.response.out.write(u"""</SELECT></td></tr>		
				<tr><td>Тех.здание:</td> <td><textarea name="tz" rows="5" cols="40"></textarea></td></tr>""") #опциональное
				
	
		self.response.out.write(u"<tr><td>Ответственный:</td> <td>%s</td></tr></table>"%pl.respWk.surname)
		
		self.response.out.write(u'Утверждают:</br>')
	
	
		wks=db.GqlQuery('SELECT * FROM Worker')
		for wk in wks:
			self.response.out.write(u"<input type=\"checkbox\" name=\"submiters\" value=\"%s\">%s</br>"%(wk.key(),wk.surname))
		
		self.response.out.write(u"""<input type="button" value="Принять" onclick="javascript:window.location.href='/order/add?eqipm='+equipment+'&quant='+document.getElementById('quant').value+'&price='+document.getElementsByName('price')[0].value+'&vendor='+document.getElementsByName('vendor')[0].value+'&status='+document.getElementsByName('status')[0].value+'&date='+document.getElementsByName('dateVend')[0].value+'&payer='+document.getElementsByName('payer')[0].value+'&tpay='+document.getElementsByName('tpaymnt')[0].value+'&tz='+document.getElementsByName('tz')[0].value+'&resp=%s'+'&ends='+getList('submiters')">%s</body></html>"""%(pl.respWk.key(), lcncss.Mtempl.end))
