# -*- coding: UTF-8-*-
import cgi
import lcncss
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class Equipment(db.Model):
	name = db.StringProperty(multiline=True)
	
	
class EqPage(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
	
	def doSmf(self):
		wk= db.get(self.request.str_cookies['session'])
		self.response.out.write(u"""<html><head>%s</head><body>%s Список оборудования:</br></br> <table border="1">"""%(lcncss.style,lcncss.beg(wk.surname)))
		eqs=db.GqlQuery('SELECT * FROM Equipment')
		
		for eq in eqs:
			self.response.out.write("<tr><td>%s</td></tr>" % (eq.name))
				
		self.response.out.write(u"""</table>
		</br>
		<form method="post" action="/equipment/add">
		Добавить оборудование:</br>
		<input name="name" size="50"><input type="submit" value="Добавить">
		</form>		
		%s</body></html>"""%lcncss.Mtempl.end)



class AddEq(webapp.RequestHandler):
	def post(self):		
			if (verify.verifyUsr(self)):
				self.doSmf()
			else:
				self.redirect('/')
						
	def doSmf(self):
		eq=Equipment()
		eq.name=self.request.get('name')
		eq.put()
		self.redirect('/equipment')
		
