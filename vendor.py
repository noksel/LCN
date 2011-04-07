# -*- coding:UTF-8 -*-
import lcncss
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class Vendor(db.Model):
	name=db.StringProperty(multiline=False)
	
class VendorPage(webapp.RequestHandler):
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
		<b>Поставщики:</b>
		<table>
		"""%(lcncss.style,lcncss.beg(wk.surname)))
		vds=db.GqlQuery('SELECT * FROM Vendor')			
		for vd in vds:
			self.response.out.write("<tr><td>%s</td></tr>"% (vd.name))
		self.response.out.write(u"""
		</table> 
		<hr>
		<form method="post" action="vendor/add">
		Добавить поставщика:<br>
		Название: <input name="name"> <input type="submit" value="Добавить">
		</form>
		%s
		</body></html>
		"""%lcncss.Mtempl.end)
		
class VendorAdd(webapp.RequestHandler):
	def post(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')		
	
	def doSmf(self):	
		vd=Vendor()
		vd.name=self.request.get('name')
		vd.put()
		self.redirect('/vendor')


