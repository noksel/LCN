#-*- coding:UTF-8 -*-
import lcncss
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class Payer(db.Model):
	name=db.StringProperty(multiline=False)
	
class PayerPage(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
				
	def doSmf(self):
		wk= db.get(self.request.str_cookies['session'])
		self.response.out.write(u"""<html><head>%s</head><body>%s <table border="1">
		<tr><th>Плательщик</th></tr>
		"""%(lcncss.style,lcncss.beg(wk.surname)))
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
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')	
				
	def doSmf(self):	
		payr=Payer(name=self.request.get('name'))
		payr.put()
		self.redirect('/payer')
