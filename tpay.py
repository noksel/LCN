#-*- coding: UTF-8 -*-

import lcncss
from google.appengine.ext import db
from google.appengine.ext import webapp

class TypePayment(db.Model):
	name=db.StringProperty()
	
class TypePayPg(webapp.RequestHandler):
	def get(self):
		self.response.out.write(u"""<html><head>%s</head><body>%sТипы оплаты: </br></br> <table border="1">"""%(lcncss.style,lcncss.Mtempl.beg))
		tps=db.GqlQuery("SELECT * FROM TypePayment")
		for tp in tps:
			self.response.out.write("<tr><td>%s</td></tr>"%(tp.name))
			
		self.response.out.write(u"""</table>
		</br><form method="post" action="/tpaymnt/add">
		Добавить название типа платежа:</br> <input name="name"> <input type="submit" value="Добавить">
		</form>		
		""")
		self.response.out.write("""%s</body></html>"""%lcncss.Mtempl.end)
		
class TypePaymntAdd(webapp.RequestHandler):
	def post(self):
		tp=TypePayment(name=self.request.get('name'))
		tp.put()
		self.redirect("/tpaymnt")
