#-*- coding:UTF-8 -*-
import lcncss
from google.appengine.ext import db
from google.appengine.ext import webapp

class Payer(db.Model):
	name=db.StringProperty(multiline=False)
	
class PayerPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write(u"""<html><head>%s</head><body>%s <div id="centre"><table border="1">
		<tr><th>Плательщик</th></tr>
		"""%(lcncss.style,lcncss.templ))
		prs=db.GqlQuery('SELECT * FROM Payer')
		
		for pr in prs:
			self.response.out.write("<tr><td>%s</td></tr>"%(pr.name))
		
		self.response.out.write(u"""</table>
		<form method="post" actio="/payer/add">
		</br>Добавить плательщика:</br>
		Название: <input name="name"> <input type="submit" value="Добавить">
		</form>
		</div></body></html>""")
		
class PayerAdd(webapp.RequestHandler):
	def post(self):
		payr=Payer(name=self.request.get('name'))
		self.redirect('/payer')
