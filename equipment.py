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
		cUsr=verify.verifyUsr(self)
 		if (cUsr!=None):
			self.doSmf(cUsr)			
		else:
			self.redirect('/')
	
	def doSmf(self,cUsr):
		
		self.response.out.write(u"""<html><head>%s</head><body>%s <div class="titlePg">Список оборудования:</div><table border="1">"""%(lcncss.style,lcncss.beg(cUsr.surname)))
		eqs=db.GqlQuery('SELECT * FROM Equipment')
		
		for eq in eqs:
			self.response.out.write("<tr><td>%s</td></tr>" % (eq.name))
				
		self.response.out.write(u"""</table></br>""")
		
		if(unicode(cUsr.key()) in verify.getList([u'Администраторы',u'Работники'])):
			self.response.out.write(u"""
		<form method="post" action="/equipment/add">
		Добавить оборудование:</br>
		<input name="name" size="50"><input type="submit" value="Добавить">
		</form>""")
		self.response.out.write(u"""
		%s</body></html>"""%lcncss.Mtempl.end)



class AddEq(webapp.RequestHandler):
	def post(self):		
		cUsr=verify.verifyUsr(self)
 		if (cUsr!=None):
			if(unicode(cUsr.key()) in verify.getList([u'Администраторы',u'Работники'])):
				self.doSmf()	
			else:		
				self.redirect('/equipment')
		else:		
			self.redirect('/equipment')
						
	def doSmf(self):
		eq=Equipment()
		eq.name=self.request.get('name')
		eq.put()
		self.redirect('/equipment')
		
