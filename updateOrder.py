# -*-  coding: UTF-8 -*-
import lcncss
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class UpdateOrderPg(webapp.RequestHandler):
	def get(self):
 		cUsr=verify.verifyUsr(self)
 		if (cUsr!=None):
			_ord=db.get(self.request.get('kord'))
			
			end=db.GqlQuery('SELECT * FROM Endorsment WHERE order=:order and submiter=:sbm',order=_ord,sbm=cUsr)
			
			if (cUsr.key()==_ord.respWk.key() or (end.count()>0 and verify.verifyRightEndors(cUsr,end[0]))):
				self.doSmf(cUsr)			
		else:
		 self.redirect('/')
			
	def doSmf(self,cUsr):
		_ord=db.get(self.request.get('kord'))
		
		self.response.out.write(u"""<html><head>%s
		<script src="/script/jquery-1.5.2.min.js"></script>
		<script src="/script/my.js"></script>
		<script type="text/javascript">
			$(document).ready( function()
			{
				$('.dis').attr('disabled',true);
				submCh=$('#submCh').remove();
				$('#enbtn').click( function()
				{
					$('.dis').attr('disabled',false);
					$('#enbtn').replaceWith(submCh);
									
				}
				);
				
					var price=''
					var calc = function(){
						$('#cost')[0].value=($('input[name=price]')[0].value*$('#quant')[0].value).toFixed(3);
					}				
					
					$('input[name=price]').keyup(calc);
					$('#quant').keyup(calc);	
					
			}			
			);
		</script>		
		<script>equipment='%s';</script>
		</head><body>%s<div class="titlePg">Правка заявки</div><table>"""%(lcncss.style,_ord.equipment.key(),lcncss.beg(cUsr.surname)))
		
		self.response.out.write(u"<tr><td>Оборудование: </td><td>%s</td></tr>"%_ord.equipment.name)
		self.response.out.write(u"<tr><td>Количество:</td> <td><input class=\"dis\" id=\"quant\" value=\"%s\"></td></tr>"%_ord.quantity)
		
		self.response.out.write(u"<tr><td>Цена(руб.):</td> <td><input class=\"dis\" name=\"price\" value=\"%s\"></td></tr>"%_ord.price)
		self.response.out.write(u"<tr><td>Стоимость:</td> <td><input DISABLED id=\"cost\" value=\"%s\"></td></tr>"%(_ord.quantity*_ord.price))

		self.response.out.write(u"<tr><td>Поставщик:</td> <td><SELECT class=\"dis\" name=\"vendor\">")
		vds =db.GqlQuery("SELECT * FROM Vendor")
		
		for vd in vds:
			if(vd.key()==_ord.vendor.key()):
				self.response.out.write(u"<OPTION SELECTED value=\"%s\">%s\n"%(vd.key(),vd.name))
			else:
				self.response.out.write(u"<OPTION value=\"%s\">%s"%(vd.key(),vd.name))
			
		self.response.out.write(u"</SELECT></td></tr>")
		self.response.out.write(u"""<tr><td>Статус заявки:</td> <td><SELECT class=\"dis\" name=\"status\">""")
		
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
		elif (_ord.status==3):
			self.response.out.write(u"""
				<OPTION value=\"0\">Черновик
				<OPTION SELECTED value=\"3\">Исполнена</SELECT></td></tr>""")			
		self.response.out.write(u"""<tr><td>Дата поставки:</td> <td><input class=\"dis\" name=\"dateVend\" value=\"%s\"></td></tr>"""%_ord.dateVend)
		
		self.response.out.write(u"<tr><td>Плательщик:</td> <td><SELECT class=\"dis\" name=\"payer\">")
		prs =db.GqlQuery("SELECT * FROM Payer")		
		for pr in prs:
			if(pr.key()==_ord.payer.key()):
				self.response.out.write(u"<OPTION SELECTED value=\"%s\">%s"%(pr.key(),pr.name))			
			else:
				self.response.out.write(u"<OPTION value=\"%s\">%s"%(pr.key(),pr.name))			
		
		self.response.out.write(u"</SELECT></td></tr>")
		
		self.response.out.write(u"""<tr><td>Тип оплаты:</td><td><SELECT class=\"dis\" name="tpaymnt">""")
		tps=db.GqlQuery("SELECT * FROM TypePayment")
		
		for tp in tps:
			if(tp.key()==_ord.typePayment.key()):
				self.response.out.write(u"<OPTION SELECTED value=\"%s\">%s"%(tp.key(),tp.name))
			else:
				self.response.out.write(u"<OPTION value=\"%s\">%s"%(tp.key(),tp.name))	
		
		self.response.out.write(u"""</SELECT></td></tr>		
				<tr><td>Тех.здание:<br/>
				(укажите ссылку на документ ТЗ):<br/>
				<a href="https://docs.google.com">https://docs.google.com</>
				
				</td> <td><input class="dis" name="tz" value="%s"></br><a href="%s">%s</a></td></tr>"""%(_ord.tz,_ord.tz,_ord.tz)) #опциональное
		
	
				
		self.response.out.write(u"<tr><td>Ответственные:</td> <td>%s</td></tr></table>"%_ord.respWk.surname)
		
		self.response.out.write(u'Утверждают:</br>')
	
	
		wks=db.GqlQuery('SELECT * FROM Worker ORDER BY surname')
		ends=db.GqlQuery('SELECT * FROM Endorsment WHERE order=:order',order=_ord)
	
		
		e=None
		for _wk in wks:
			tmp=False
			allEnd=True
			sbm=""
			for end in ends:
				if(end.submit==False):
					allEnd=False
									
				if (_wk.key()==end.submiter.key()):
					if (end.submit==True):
						sbm=u"(Одобрил)"
					if(verify.verifyRightEndors(cUsr,end) and end.submit==False): 
						e=end
					tmp=True
					break
			if(tmp==True):
				if(_wk.key()!=_ord.respWk.key()):
					
					if(unicode(_wk.key()) in verify.getList([u'Работники'])):
						self.response.out.write(u"<input class=\"dis\" CHECKED type=\"checkbox\" name=\"submiters\" value=\"%s\">%s %s</br>"%(_wk.key(),_wk.surname,sbm))		
			else:
				if(_wk.key()!=_ord.respWk.key()):					
					if(unicode(_wk.key()) in verify.getList([u'Работники'])):
						self.response.out.write(u"<input class=\"dis\" type=\"checkbox\" name=\"submiters\" value=\"%s\">%s</br>"%(_wk.key(),_wk.surname))
		
		
		
		if(cUsr.key()==_ord.respWk.key()):
			if(_ord.status==0 or _ord.status==1):
		 		self.response.out.write(u"<div class=\"notice\">Уважаемые коллеги! если заявка находится на одобрении и вы решили изменить какие-то данные то все \"Подтверждения\" на закупку будут сброшены. </div>")
		 		self.response.out.write(u"<input id=\"enbtn\"type=\"button\" name=\"enable\" value=\"Разблокировать для изменения\">")
		 		self.response.out.write(u"""<div id="submCh"><input type="button" value="Принять изменения" onclick="javascript:
		 		(function(){
		 		
		 		if($('select[name=status]')[0].value==1 && $('input[name=price]')[0].value=='')
		 alert('Введите цену');
		
		else if($('select[name=status]')[0].value==1 && $('input[name=dateVend]')[0].value=='')
		 alert('Введите дату поставки');
		
		else if($('select[name=status]')[0].value==1 && $('input[name=tz]')[0].value=='')
		 alert('Введите ccылку на ТЗ');
		
		else if(!checkCount('submiters'))
			alert('Отметте кто утверждает заявку');
			
		
		else
		{
		 		window.location.href='/order/update?ord=%s'+'&quant='+document.getElementById('quant').value+'&price='+document.getElementsByName('price')[0].value+'&vendor='+document.getElementsByName('vendor')[0].value+'&status='+document.getElementsByName('status')[0].value+'&date='+document.getElementsByName('dateVend')[0].value+'&payer='+document.getElementsByName('payer')[0].value+'&tpay='+document.getElementsByName('tpaymnt')[0].value+'&tz='+document.getElementsByName('tz')[0].value+'&resp=%s'+'&ends='+getList('submiters')
		 }		
		 		})()">"""%(_ord.key(),_ord.respWk.key()))
		 		self.response.out.write(u"""<input type="button" value="Удалить заявку" onclick="javascript:window.location.href='/order/dell?ord=%s';" > </div>"""%(_ord.key()))
		 	elif(_ord.status==2):
		 		self.response.out.write(u"""<input type="button" value="Исполнена" onclick="javascript:window.location.href='/order/tohist?ord=%s';" > """%(_ord.key()))
		 		self.response.out.write(u"""<input type="button" value="Удалить заявку" onclick="javascript:window.location.href='/order/dell?ord=%s';" > """%(_ord.key()))
		 
		if(e):
			self.response.out.write(u"<input type=\"button\" name=\"endsmnt\" value=\"Одобрить\" onclick=\"javascript:window.location.href='/order/submit?endsmnt=%s'\">"%(e.key()))
			
		self.response.out.write(u"""%s</body></html>"""%(lcncss.Mtempl.end))
