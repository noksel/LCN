#-*- coding:UTF-8 -*-

from google.appengine.ext import db
from google.appengine.ext import webapp

class Payer(db.Model):
	name=db.StringProperty(multiline=False)
	
class PayerPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write("""<html><body><table>""")
		prs=db.GqlQuery('SELECT * FROM Payer')
		
		if(prs.count()==0):
			self.init()
			prs=db.GqlQuery('SELECT * FROM Payer')
		for pr in prs:
			self.response.out.write("<tr><td>%s</td><td>%s</td></tr>"%(pr.name,pr.key()))
		
		self.response.out.write("""</table></body></html>""")
		
	def init(self):
		pr=Payer(name=u'ОКБ РВТ')
		pr.put()
		
		pr=Payer(name=u'Гиком')
		pr.put()
		
		pr=Payer(name=u'ЛКН(НГТУ)')
		pr.put()
