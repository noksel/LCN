# −*− coding: UTF−8 −*−

import lcncss
from google.appengine.ext import db
from google.appengine.ext import webapp

class Worker(db.Model):
 surname = db.StringProperty(multiline=False)
 patronymic=db.StringProperty()
 name = db.StringProperty(multiline=False)
 email = db.StringProperty(multiline=False)
 phone=db.StringProperty(multiline=False)

class WorkersPage(webapp.RequestHandler):
 def get(self):
	self.response.out.write("""<html>
														%s
														<body>%s"""%(lcncss.style,lcncss.Mtempl.beg))
	wks=db.GqlQuery('SELECT * FROM Worker')
	self.response.out.write(u'Список сотрудников лаборатории:</br></br>')
	self.response.out.write('<table border="1">')
	self.response.out.write(u"""
														<tr><th>Фамилия</th><th>Отчество</th><th>Имя</th><th>E-mail</th><th>Телефон</th> </tr>
														""")

	for wk in wks:
		self.response.out.write("<tr><td>%s</br></td><td>%s</br><td>%s</br></td><td><a href=\"mailto:%s\">%s</a></td><td>%s</td></tr>"%(wk.surname,wk.name,wk.patronymic,wk.email,wk.email,wk.phone))	
			
	self.response.out.write('</table></br>')

	
	
	self.response.out.write(u"""
			<form method="post" action="/workers/add">
				<div>Добавить сотрудника</div>
				<div>
				<div style="float:left; height:100%; line-height:26px;">
				Фамилия: </br>
				Имя:</br>
				Отчество:</br>
				E-mail:</br>
				Телефон:</br>
				</div>
				<div>
					<input name="surname"></br>
					<input name="name"></br>
					<input name="patronymic"></br>
					<input name="email"></br>
					<input name="phone"></br>					
				</div>
				</div>
				<input type="submit" value="Добавить">
			</form>""")

	self.response.out.write("""%s</body></html>"""%lcncss.Mtempl.end)

class AddWorker(webapp.RequestHandler):
	def post(self):
		wk=Worker()
		wk.surname=self.request.get('surname')
		wk.patronymic=self.request.get('patronymic')
		wk.name=self.request.get('name')
		wk.email=self.request.get('email')
		wk.phone=self.request.get('phone')
		wk.put()
		self.redirect('/workers')
	
	
	
