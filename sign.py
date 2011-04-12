# -*- coding: UTF-8 -*-
import workers
from google.appengine.ext import db
from google.appengine.ext import webapp
import datetime

class Login(webapp.RequestHandler):
	def get(self):
		
		if(("session" in self.request.str_cookies) and (self.request.str_cookies['session']!="")):
			try:
				wk= db.get(self.request.str_cookies['session'])
				"%s"%wk.surname
				self.redirect('/')				
			except (db.BadKeyError, AttributeError):
			 self.CreateLgPg()			
		else:
			self.CreateLgPg()

	def CreateLgPg(self):	
		self.response.out.write("""
		<html>
		<style>
			#frm
			{
				position: absolute;
				left:35%;
				top: 30%;
				background-color: #45A6F2;
				border-width:thin;
				
				padding-top:20px;
				padding-bottom:10px;
				padding-left:20px;
				padding-right:20px;
			}
			#table
			{
			display:table;
			}
			div.row
			{
			display:table-row;
			}
			div.cell
			{
			display:table-cell;
			}
		</style>
			<body>
			<div id="frm">
				<form method="post" action="/sign">
					<div id="table">
						<div class="row"><div class="cell">E-mail:</div> <div class="cell"><input name="email"></div></div>
						<div class="row"><div class="cell">Пароль:</div> <div class="cell"><input name="passwd" type="password"></div></div>
					</div>
					<input type="checkbox" name="longsess" value="True"> Оставаться в системе<br/>

					<br/>
					<input type="submit" value="Войти">
					
				</form>
			</div>
			</body>
		</html>		
		""")
		
		
		
class Sign(webapp.RequestHandler):
	def post(self):
		
		wks=db.GqlQuery("SELECT * FROM Worker WHERE email=:email",email=self.request.get('email'))
		if(wks.count()>0):
			wk=wks[0]		
			pswd=self.request.get('passwd')
			if (pswd==wk.passwd and self.request.get('longsess')=="True"):
				m=datetime.date.today()+datetime.timedelta(days=30)
				self.response.headers.add_header('Set-Cookie',"session=%s; path=/; expires=%s;"%(wk.key(),m.strftime("%a, %d %b %Y %T GTM")))
			else:
				self.response.headers.add_header('Set-Cookie',"session=%s; path=/;"%(wk.key()))
				

		self.redirect('/')
class Logout(webapp.RequestHandler):
	def get(self):
		self.response.headers.add_header('Set-Cookie',"session=; path=/;")
		self.redirect('/')
