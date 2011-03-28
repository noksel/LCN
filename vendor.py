# -*- coding:UTF-8 -*-
import lcncss
from google.appengine.ext import db
from google.appengine.ext import webapp

class Vendor(db.Model):
	name=db.StringProperty(multiline=False)
	
class VendorPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write(u"""
		<html>
		<head>
			%s
		</head>
		<body>
		%s		
		<dif id="centre">
		<b>Поставщики:</b>
		<table>
		"""%(lcncss.style,lcncss.templ))
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
		</div>
		</body></html>
		""")
		
class VendorAdd(webapp.RequestHandler):
	def post(self):
		vd=Vendor()
		vd.name=self.request.get('name')
		vd.put()
		self.redirect('/vendor')


