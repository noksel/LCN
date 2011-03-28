#-*- coding: UTF-8 -*-

import lcncss
from google.appengine.ext import db
from google.appengine.ext import webapp

class TypePayment(db.Model):
	name=db.StringProperty()
	
class TypePayPg(webapp.RequestHandler):
	def get(self):
		self.response.out.write(u"""<html><head>%s</head><body>%s <div id="centre">Типы оплаты </br></br>"""%(lcncss.style,lcncss.templ))
		tps=db.GqlQuery("SELECT * FROM TypePayment")
		for tp in tps:
			self.response.out.write("%s</br>"%(tp.name))
			
		self.response.out.write(u"""
		</br><form method="post" action="/tpaymnt/add">
		Название типа платежа: <input name="name"> <input type="submit" value="Добавить">
		</form>		
		""")
		self.response.out.write(""" </div></body></html>""")
		
class TypePaymntAdd(webapp.RequestHandler):
	def post(self):
		tp=TypePayment(name=self.request.get('name'))
		tp.put()
		self.redirect("/tpaymnt")
