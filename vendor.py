# -*- coding:UTF-8 -*-

from google.appengine.ext import db
from google.appengine.ext import webapp

class Vendor(db.Model):
	name=db.StringProperty(multiline=False)
	
class VendorPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write("""
		<html><body><table>
		""")
		vds=db.GqlQuery('SELECT * FROM Vendor')
		if (vds.count()==0):
			self.init()
			vds=db.GqlQuery('SELECT * FROM Vendor')
			
		for vd in vds:
			self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"% (vd.name,vd.key()))
		self.response.out.write("""
		</table></body></html>
		""")
	def init(self):
		vd = Vendor(name=u"ООО \"Абтроникс\"")
		vd.put()
		
		vd = Vendor(name=u"ООО \"Миком\"")
		vd.put()
		vd = Vendor(name=u"ЗАО \"Радэком\"")
		vd.put()
		vd = Vendor(name=u"ООО \"Рубикон\"")
		vd.put()
