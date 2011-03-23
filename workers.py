# −*− coding: UTF−8 −*−

import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp

class Worker(db.Model):
 surname = db.StringProperty(multiline=False)
 name = db.StringProperty(multiline=False)
 email = db.StringProperty(multiline=False)
 phoneNamb=db.StringProperty(multiline=False)

class WorkersPage(webapp.RequestHandler):
 def get(self):
	self.response.out.write("""<html>
														
														<body>""")
	wks=db.GqlQuery('SELECT * FROM Worker')
	if wks.count()==0:
		self.init()
		wks=db.GqlQuery('SELECT * FROM Worker')
	self.response.out.write(u'Список сотрудников лаборатории</br>')
	self.response.out.write('<table>')
		
	for wk in wks:
		self.response.out.write('<tr>')
		
		self.response.out.write('<td>')
		self.response.out.write("%s</br>" % wk.surname)
		self.response.out.write('</td>')

		self.response.out.write('<td>')
		self.response.out.write("%s</br>" % wk.name)
		self.response.out.write('</td>')
		
		self.response.out.write('<td>')
		self.response.out.write("<a href=\"mailto:%s\">%s</a></br>" % (wk.email,wk.email))
		self.response.out.write('</td>')

				
		self.response.out.write('</tr>')
	self.response.out.write('</table>')
	self.response.out.write("""</body></html> """)
 def init(self):
 	wk=Worker()
	wk.surname =u'Петров'
	wk.name = u'Пётр'
	wk.email = 'petr@mail.ru'
	wk.phoneNamb="+7"
	wk.put()

	wk=Worker()
	wk.surname =u"Иванов"
	wk.name = u"Иван"
	wk.email = "ivan@mail.ru"
	wk.phoneNamb="+7"
	wk.put()
	wk = ()
