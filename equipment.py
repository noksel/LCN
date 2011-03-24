# -*- coding: UTF-8-*-
import cgi

from google.appengine.ext import db
from google.appengine.ext import webapp

class Equipment(db.Model):
	name = db.StringProperty(multiline=True)
	
	
class EqPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write("""<html><body>""")
		eqs=db.GqlQuery('SELECT * FROM Equipment')
		#db.delete(eqs) удаление всего
		if eqs.count()==0:
			self.init()
			eqs=db.GqlQuery('SELECT * FROM Equipment')
		
		for eq in eqs:
			self.response.out.write("%s %s</br>" % (eq.name,eq.key()))
				
		self.response.out.write("""</body></html>""")		
	def init(self):
		eq=Equipment()
		eq.name=u'Пины HPA-OJ,SPR-OW-1'
		eq.put()
		eq=Equipment()
		eq.name=u'Микросхемы'
		eq.put()
		eq=Equipment()
		eq.name=u'Резисторы'
		eq.put()
		eq=Equipment()
		eq.name=u'ЛОВ ОВ-65'
		eq.put()
