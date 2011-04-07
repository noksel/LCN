# -*- coding: UTF-8 -*-
import equipment
import workers
import lcncss
import my_js
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class PlanEq(db.Model):
	equipment=db.ReferenceProperty(equipment.Equipment)
	quantity=db.IntegerProperty()
	comment=db.StringProperty()
	resp=db.ListProperty(str)
	
class PlanEqPage(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
				
	def doSmf(self):
		wk= db.get(self.request.str_cookies['session'])
		self.response.out.write(u"""<html><head>%s </head><body>%s
		"""%(lcncss.style,lcncss.beg(wk.surname)))
		
		peqs=db.GqlQuery('SELECT * FROM PlanEq')	
		self.response.out.write(u"""<table border="1">
														<tr><th>Название</th><th>Колличество</th><th>Комментарий</th><th>Ответственные</th></tr>""")
		for peq in peqs:			
			self.response.out.write(u"<tr> <td>%s<a href=\"/planeq/to-order?kplan=%s\">(Создать заявку)</></td> <td>%s</td><td>%s</td>" % (peq.equipment.name,peq.key(),peq.quantity,peq.comment))
			mstr=str()
			self.response.out.write("<td>")
			mstr=" ".join([db.get(wrkey).surname for wrkey in peq.resp])			
			self.response.out.write("%s</td></tr>" % (mstr))							
		
		self.response.out.write(u'</table><a href="pgplaneqadd">Добавить оборудование в план</a> ')
		self.response.out.write(u"""%s</body></html>"""%lcncss.Mtempl.end)
		
class PgPlanEqAdd(webapp.RequestHandler):
 def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/') 
 
 def doSmf(self):
	wk= db.get(self.request.str_cookies['session']) 
	self.response.out.write(u"""<html><head>%s
	<script language="javascript">%s
	</script>
	</head><body>%s
	<form method="get" action="/planeq/planeqadd"><div id="centre">
	Оборудование: <SELECT style="width: 200px;" name="eqid">"""%(lcncss.style,my_js.getChList,lcncss.beg(wk.surname)))
	
	eqs=db.GqlQuery('SELECT * FROM Equipment')
	for eq in eqs:
		self.response.out.write(u"	<OPTION VALUE=\"%s\">%s"%(eq.key(),eq.name))
	self.response.out.write(u'</SELECT></br>Ответственные:</br>')
	
	
	wks=db.GqlQuery('SELECT * FROM Worker')
	for wk in wks:
		self.response.out.write(u"<input type=\"checkbox\" name=\"worker\" value=\"%s\">%s</br>"%(wk.key(),wk.surname))
	
	self.response.out.write(u"""
		Количество:<input name="quant"></br>
		Коментарий:<input name="comment"></br>
		<input value="Добавить" type="button" onclick="javascript:(function(){
		sl=document.getElementsByName('eqid');
		str='/planeq/add?eqid=';
		str=str+sl[0].value;	
		inp=document.getElementsByName('quant');
		str=str+'&quant='+inp[0].value;	
		inp=document.getElementsByName('comment');
		str=str+'&comment='+inp[0].value+'&resp=';		
		str=str+getList('worker');
		window.location.href=str})()">
		""")

	
	self.response.out.write("""</form>%s</body></html> """%(lcncss.Mtempl.end))
	
	
class PEAdd(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')	
	def doSmf(self):
		pe=PlanEq()
		pe.equipment=db.get(self.request.get('eqid'))
		pe.quantity=int(self.request.get('quant'))
		pe.comment=self.request.get('comment')
		
		
		pe.resp=self.request.get('resp').split(':')
	
		pe.put()
		self.redirect('/planeq')
		
