#-*- coding: UTF-8 -*-
import workers
import lcncss
import verify
import order
from google.appengine.ext import db
from google.appengine.ext import webapp

class GroupsPage(webapp.RequestHandler):
	def get(self):
		getUsr=verify.verifyUsr(self)
 		if (getUsr!=None):
			self.doSmf(getUsr)			
		else:
			self.redirect('/')
				
	def doSmf(self,cUsr):
		
		self.response.out.write(u"""
		<html>
		<head>
			%s
		</head>
		<body>
		%s
		<div class="titlePg">Группы:</div>
		<table>
		"""%(lcncss.style,lcncss.beg(cUsr.surname)))
		grps=db.GqlQuery('SELECT * FROM Group')			
		for gr in grps:
			self.response.out.write("<tr><td>%s</td></tr>"% (gr.name))
		
		
		self.response.out.write(u"""</table> <hr>""")
		
		if(unicode(cUsr.key()) in verify.getList([u'Администраторы'])):
			self.response.out.write(u"""<form method="post" action="/groups/add">
		Добавить группу:<br>
		Название: <input name="name"> <input type="submit" value="Добавить">
		</form>""")
		
		self.response.out.write(u"""%s</body></html>"""%lcncss.Mtempl.end)
		
class GroupAdd(webapp.RequestHandler):
	def post(self):
		cUsr=verify.verifyUsr(self)
 		if (cUsr!=None):
			if(unicode(cUsr.key()) in verify.getList([u'Администраторы'])):
				self.doSmf()
		else:					
			self.redirect('/groups')		
	
	def doSmf(self):	
		vd=workers.Group()
		vd.name=self.request.get('name')
		vd.put()
		self.redirect('/groups')
