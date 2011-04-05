# -*- coding: UTF-8 -*-
import workers
from google.appengine.ext import db
from google.appengine.ext import webapp

class Login(webapp.RequestHandler):
	def get(self):
		
		if(("session" in self.request.str_cookies) and (self.request.str_cookies['session']!="")):
			wk= db.get(self.request.str_cookies['session'])
			self.response.out.write("""%s"""%wk.surname)
		else:
			self.response.out.write("""
		<html>
			<body>
				<form method="post" action="/sign">
					E-mail: <input name="email"><br/>
					Пароль: <input name="passwd" type="password">
					<input type="submit" value="Войти">
				</form>
			</body>
		</html>		
		""")
		
		
		
class Sign(webapp.RequestHandler):
	def post(self):
		
		wks=db.GqlQuery("SELECT * FROM Worker WHERE email=:email",email=self.request.get('email'))
		wk=wks[0]
		
		pswd=self.request.get('passwd')
		if (pswd==wk.passwd):
			self.response.headers.add_header('Set-Cookie',"session=%s; path=/; expires=Sunday, 30-Apr-2011 23:59:59 GMT;"%wk.key())
			self.redirect('/')

