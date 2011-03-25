# −*− coding: UTF−8 −*−
import equipment
import workers
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp

class PgPlanEqAdd(webapp.RequestHandler):
 def get(self):
	self.response.out.write(u"""<html>	<body>
	<form method="get" action="/planeq/planeqadd">
	Оборудование:<SELECT NAME="eqid">""")
	
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
		str='http://localhost:8080/planeq/planeqadd?eqid=';
		str=str+sl[0].value;		
	
		inp=document.getElementsByName('quant');
		str=str+'&quant='+inp[0].value;	
		inp=document.getElementsByName('comment');
		str=str+'&comment='+inp[0].value+'&resp=';	
		
		cht=document.getElementsByName('worker')
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
			str=str+astr;
		window.location.href=str})()">
		""")

	
	self.response.out.write("""</form></body></html> """)
													
