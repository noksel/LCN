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
	respWk=db.ReferenceProperty(workers.Worker)
	
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
			crOrd=""
			if (wk.key()==peq.respWk.key() ):
			 crOrd=u"<a href=\"/planeq/to-order?kplan=%s\">(Создать заявку)</a>"%peq.key()			
			
			self.response.out.write(u"<tr> <td>%s %s</td> <td>%s</td><td>%s</td>" % (peq.equipment.name,crOrd,peq.quantity,peq.comment))

			self.response.out.write("<td>%s</td></tr>" % (peq.respWk.surname))							
		
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
	<script src="/script/my.js"></script>
	</head><body>%s
	<form method="get" action="/planeq/planeqadd"><div id="centre">
	Оборудование: <SELECT style="width: 200px;" name="eqid">"""%(lcncss.style,lcncss.beg(wk.surname)))
	
	eqs=db.GqlQuery('SELECT * FROM Equipment ORDER BY name')
	for eq in eqs:
		self.response.out.write(u"	<OPTION VALUE=\"%s\">%s"%(eq.key(),eq.name))
	self.response.out.write(u'</SELECT></br>Ответственный:')
	
	self.response.out.write(u'<SELECT name=\"resp\">')
	wks=db.GqlQuery('SELECT * FROM Worker ORDER BY surname')
	for wk in wks:
		self.response.out.write(u"<OPTION value=\"%s\">%s</br>"%(wk.key(),wk.surname))
	self.response.out.write(u'</SELECT><br/>')
	
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
		str=str+document.getElementsByName('resp')[0].value;
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
		
		
		pe.respWk=db.get(self.request.get('resp'))
	
		pe.put()
		self.redirect('/planeq')
		
