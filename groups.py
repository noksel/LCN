#-*- coding: UTF-8 -*-
import workers
import lcncss
import verify
import order
from google.appengine.ext import db
from google.appengine.ext import webapp

class GroupsPage(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
				
	def doSmf(self):
		wk= db.get(self.request.str_cookies['session'])
		self.response.out.write(u"""
		<html>
		<head>
			%s
		</head>
		<body>
		%s
		<b>Группы:</b>
		<table>
		"""%(lcncss.style,lcncss.beg(wk.surname)))
		grps=db.GqlQuery('SELECT * FROM Group')			
		for gr in grps:
			self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"% (gr.name,gr.key()))
		self.response.out.write(u"""
		</table> 
		<hr>
		<form method="post" action="/groups/add">
		Добавить группу:<br>
		Название: <input name="name"> <input type="submit" value="Добавить">
		</form>
		%s
		</body></html>
		"""%lcncss.Mtempl.end)
		
class GroupAdd(webapp.RequestHandler):
	def post(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')		
	
	def doSmf(self):	
		vd=workers.Group()
		vd.name=self.request.get('name')
		vd.put()
		self.redirect('/groups')
