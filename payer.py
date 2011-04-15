#-*- coding:UTF-8 -*-
import lcncss
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class Payer(db.Model):
	name=db.StringProperty(multiline=False)
	
class PayerPage(webapp.RequestHandler):
	def get(self):
		getUsr=verify.verifyUsr(self)
 		if (getUsr!=None):
			self.doSmf(getUsr)			
		else:
			self.redirect('/')
				
	def doSmf(self, cUsr):
		
		self.response.out.write(u"""<html><head>%s</head><body>%s <div class="titlePg">Список плательщиков:</div> <table border="1">
		<tr><th>Плательщик</th></tr>
		"""%(lcncss.style,lcncss.beg(cUsr.surname)))
		prs=db.GqlQuery('SELECT * FROM Payer')
		
		for pr in prs:
			self.response.out.write("<tr><td>%s</td></tr>"%(pr.name))
		
		self.response.out.write(u"""</table>
		<form method="post" action="/payer/add">
		</br>Добавить плательщика:</br>
		Название: <input name="name"> <input type="submit" value="Добавить">
		</form>
		%s</body></html>"""%lcncss.Mtempl.end)
		
class PayerAdd(webapp.RequestHandler):
	def post(self):
		getUsr=verify.verifyUsr(self)
 		if (getUsr!=None):
			self.doSmf()			
		else:
			self.redirect('/')	
				
	def doSmf(self):	
		payr=Payer(name=self.request.get('name'))
		payr.put()
		self.redirect('/payer')
