# −*− coding: UTF−8 −*−

import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp

class Worker(db.Model):
 surname = db.StringProperty(multiline=False)
 name = db.StringProperty(multiline=False)
 email = db.StringProperty(multiline=False)
 phone=db.StringProperty(multiline=False)

class WorkersPage(webapp.RequestHandler):
 def get(self):
	self.response.out.write("""<html>
														
														<body>""")
	wks=db.GqlQuery('SELECT * FROM Worker')
	#db.delete(wks)
	if wks.count()==0:
		self.init()
		wks=db.GqlQuery('SELECT * FROM Worker')
	self.response.out.write(u'Список сотрудников лаборатории</br>')
	self.response.out.write('<table border="1">')
	self.response.out.write(u"""
														<tr><th>Фамилия</th> <th>Имя</th> <th>E-mail</th> <th>Телефон</th> </tr>
														""")

	for wk in wks:
		self.response.out.write('<tr>')
		
		self.response.out.write('<td>')
		self.response.out.write("%s</br>" % wk.surname)
		self.response.out.write('</td>')

		self.response.out.write('<td>')
		self.response.out.write("%s</br>" % wk.name)
		self.response.out.write('</td>')
		
		self.response.out.write('<td>')
		self.response.out.write("<a href=\"mailto:%s\">%s</a>" % (wk.email,wk.email))
		self.response.out.write('</td>')
		
		
		self.response.out.write("<td>%s</td><td>%s</td>" % (wk.phone,wk.key()))
		
						
		self.response.out.write('</tr>')
		
	self.response.out.write('</table></br>')

	
	
	self.response.out.write(u"""
			<form method="post" action="/workers/add">
				<div>Добавить сотрудника</div>
				Фамилия: <input name="surname"></br>
				Имя: <input name="name"></br>
				E-mail: <input name="email"></br>
				Телефон: <input name="phone"></br>
				<input type="submit" value="Добавить">	
			</form>""")

	self.response.out.write("""</body></html> """)
 def init(self):
 	wk=Worker(surname=u"Соколов")	
	wk.put()

	wk=Worker(surname=u"Коротаев")	
	wk.put()
	
	wk=Worker(surname=u"Большаков")	
	wk.put()
	wk=Worker(surname=u"Абашин")	
	wk.put()
	wk=Worker(surname=u"Штанюк")	
	wk.put()
	wk=Worker(surname=u"Вдовин")	
	wk.put()
	
	
	
	
