# -*-  coding: UTF-8 -*-
from google.appengine.ext import db
from google.appengine.ext import webapp

class ToOrderPage(webapp.RequestHandler):
	def get(self):
		pl=db.get(self.request.get('kplan'))
		self.response.out.write(u"""<html><head><script>equipment='%s';host='http://localhost:8080';
		function getList(chName)
		 {
		 	cht=document.getElementsByName(chName)
			 astr='';
		 	for(var i=0;i<cht.length;i++)
		 	{
				
				if (cht[i].checked)
				 {
				  if(astr=='')
				 		astr=cht[i].value
				 	else
				 		astr=astr+':'+cht[i].value
				 }
			}
			return astr;
		};
		</script></head><body><b>Создание заявки</b><table>"""%pl.equipment.key())
		self.response.out.write(u"<tr><td>Оборудование: </td><td>%s</td></tr>"%pl.equipment.name)
		self.response.out.write(u"<tr><td>Количество:</td> <td><input id=\"quant\" value=\"%s\"></td></tr>"%pl.quantity)
		
		self.response.out.write(u"<tr><td>Цена:</td> <td><input name=\"price\"</td></tr>")

		self.response.out.write(u"<tr><td>Поставщик:</td> <td><SELECT name=\"vendor\">")
		vds =db.GqlQuery("SELECT * FROM Vendor")
		
		for vd in vds:
			self.response.out.write(u"<OPTION value=\"%s\">%s"%(vd.key(),vd.name))
			
		self.response.out.write(u"</SELECT></td></tr>")
		self.response.out.write(u"""<tr><td>Статус заявки:</td> <td><SELECT name=\"status\">
				<OPTION value=\"0\">Черновик
				<OPTION value=\"1\">На одобрение</SELECT></td></tr>
				<tr><td>Дата поставки:</td> <td><input name=\"dateVend\"></td></tr>
				<tr><td>Тип оплаты:</td> <td><input name=\"typePayment\"></td></tr>
				<tr><td>Тех.здание:</td> <td>опциональное</td></tr>""") #опциональное
				
		mstr=str()
		for p in pl.resp:
				mstr=mstr+"%s "%db.get(p).surname		
		self.response.out.write(u"<tr><td>Ответственные:</td> <td>%s</td></tr></table>"%mstr)
		
		self.response.out.write(u'Утверждают:</br>')
	
	
		wks=db.GqlQuery('SELECT * FROM Worker')
		for wk in wks:
			self.response.out.write(u"<input type=\"checkbox\" name=\"submiters\" value=\"%s\">%s</br>"%(wk.key(),wk.surname))
		
		self.response.out.write(u"""<input type="button" value="Принять" onclick="javascript:window.location.href=host+'/order/add?eqipm='+equipment+'&quant='+document.getElementById('quant').value+'&price='+document.getElementsByName('price')[0].value+'&vendor='+document.getElementsByName('vendor')[0].value+'&status='+document.getElementsByName('status')[0].value+'&date='+document.getElementsByName('dateVend')[0].value+'&tpay='+document.getElementsByName('typePayment')[0].value+'&resp=%s'+'&ends='+getList('submiters')"></body></html>"""%(":".join(pl.resp)))
