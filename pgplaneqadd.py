# −*− coding: UTF−8 −*−
import equipment
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
	self.response.out.write('</SELECT></br>')
	
	self.response.out.write(u"""
		Количество:<input name="quant"></br>
		Коментарий:<input name="comment"></br>
		<input type="submit" value="submit">
		""")
	
	
	self.response.out.write("""</form></body></html> """)
													
