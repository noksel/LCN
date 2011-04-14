# -*- coding: UTF-8 -*-
import equipment
import workers
import lcncss
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class PlanEq(db.Model):
	equipment=db.ReferenceProperty(equipment.Equipment)
	quantity=db.IntegerProperty()
	comment=db.StringProperty()
	respWk=db.ReferenceProperty(workers.Worker)
	dateAdd = db.DateTimeProperty(auto_now_add=True)
	
class PlanEqPage(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
				
	def doSmf(self):
		wk= db.get(self.request.str_cookies['session'])
		self.response.out.write(u"""<html><head>%s
		<script src="/script/jquery-1.5.2.min.js"></script>
		 </head><body>%s<div class="titlePg">План закупок оборудования:</div>"""%(lcncss.style,lcncss.beg(wk.surname)))
		
		peqs=db.GqlQuery('SELECT * FROM PlanEq')	
		self.response.out.write(u"""<table border="1">
														<tr><th></th><th>Название</th><th>Колличество</th><th>Комментарий</th><th>Ответственные</th></tr>""")
		for peq in peqs:
			crOrd=""
			delPg=""
			if (wk.key()==peq.respWk.key() ):
			 crOrd=u"<a href=\"/planeq/to-order?kplan=%s\">(Создать заявку)</a>"%peq.key()
			 delPg=u"""<a href=\"javascript:(function(){
			 															$.post('/planeq/del',{pkey: '%s'});
			 															 window.location.href='/planeq';
			 															})()\">X</a>"""%peq.key()			
			
			self.response.out.write(u"<tr><td>%s</td> <td>%s %s</td> <td>%s</td><td>%s</td>" % (delPg,peq.equipment.name,crOrd,peq.quantity,peq.comment))

			self.response.out.write("<td><a href=\"/workers/workerPg?wkey=%s\">%s</a></td></tr>" % (peq.respWk.key(),peq.respWk.surname))							
		
		self.response.out.write(u'</table><a href="pgplaneqadd">Добавить оборудование в план</a> ')
		self.response.out.write(u"""%s</body></html>"""%lcncss.Mtempl.end)
		
class PgPlanEqAdd(webapp.RequestHandler):
 def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/') 
 
 def doSmf(self):
	cUsr= db.get(self.request.str_cookies['session']) 
	self.response.out.write(u"""<html><head>%s
	<script src="/script/my.js"></script>
	<script src="/script/jquery-1.5.2.min.js"></script>
	<script type="text/javascript">
	$(document).ready( function()
	{
		$('select[name=eqid]').change(function()
			{
				if($('select[name=eqid]')[0].value=='none')
					{$('#eqname').attr('disabled',false);}
				else {$('#eqname').attr('disabled',true);}
			}
		)
	}	
	);
	</script>
	</head><body>%s <div class="titlePg"> Добавить оборудование в план:</div>
	<form method="get" action="/planeq/planeqadd"><div id="centre">
	Оборудование: <SELECT style="width: 200px;" name="eqid">"""%(lcncss.style,lcncss.beg(cUsr.surname)))
	
	eqs=db.GqlQuery('SELECT * FROM Equipment ORDER BY name')
	for eq in eqs:
		self.response.out.write(u"	<OPTION VALUE=\"%s\">%s"%(eq.key(),eq.name))
	
	self.response.out.write(u"	<OPTION VALUE=\"none\">----Ввести своё----")
	self.response.out.write(u'</SELECT>')
	
	self.response.out.write(u'<br/><div style="width:110px;float:left;">&nbsp</div><input id="eqname" name="eqname" style="width:200px;" DISABLED>')	
	
	self.response.out.write(u'</br>Ответственный:')	
	self.response.out.write(u'<SELECT name=\"resp\">')
	wks=db.GqlQuery('SELECT * FROM Worker ORDER BY surname')
	
	
	for wk in wks:
		if(unicode(cUsr.key()) in verify.getList([u'Администраторы']) and unicode(wk.key()) in verify.getList([u'Ответственные']) ):
			self.response.out.write(u"<OPTION value=\"%s\">%s</br>"%(wk.key(),wk.surname))
		elif(unicode(cUsr.key()) in verify.getList([u'Ответственные']) and wk.key()==cUsr.key()):
			self.response.out.write(u"<OPTION value=\"%s\">%s</br>"%(wk.key(),wk.surname))
			
	self.response.out.write(u'</SELECT><br/>')
	
	self.response.out.write(u"""
		Количество:<input name="quant"></br>
		Коментарий:<input name="comment"></br>
		<input value="Добавить" type="button" onclick="javascript:(function(){
		str='/planeq/add?';
		
		if($('select[name=eqid]')[0].value=='none')
			{
				str=str+'eqname='+$('#eqname')[0].value;
			}
		else
		{
			sl=document.getElementsByName('eqid');
			str=str+'eqid='+sl[0].value;	
		}
			
		
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
		
		if (self.request.get('eqid')!=""):
			pe.equipment=db.get(self.request.get('eqid'))
		
		elif(self.request.get('eqname')!=""):
			eq=equipment.Equipment()
			eq.name=self.request.get('eqname')
			eq.put()
			pe.equipment=eq		
		pe.quantity=int(self.request.get('quant'))
		pe.comment=self.request.get('comment')
		
		
		pe.respWk=db.get(self.request.get('resp'))
	
		pe.put()
		self.redirect('/planeq')
		
class PEDel(webapp.RequestHandler):
	def post(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')	
			
	def doSmf(self):
		pe=db.get(self.request.get('pkey'))
		db.delete(pe)
		
