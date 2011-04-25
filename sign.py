# -*- coding: UTF-8 -*-
import workers
import datetime
import hashlib
import random
import verify

from google.appengine.ext import db
from google.appengine.ext import webapp


class Session(db.Model):
	session =db.StringProperty()
	dateEnd= db.DateProperty()
	user= db.ReferenceProperty(workers.Worker)

class Login(webapp.RequestHandler):
	def get(self):
		getUsr=verify.verifyUsr(self)
 		if (getUsr!=None):
			self.redirect('/')					
		else:
			self.CreateLgPg()


	def CreateLgPg(self):	
		self.response.out.write("""
		<html>
		<style>
			body
			{
			background-color:#1f66c0;
			
			}
			
			#frm
			{
				position: absolute;
				left:35%;
				top: 30%;
				color: white;
				background-color: #0c3569;
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
					<input style="float:right;" type="submit" value="Войти">
					
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
			
			sess=Session()
			sess.session=hashlib.md5(u"".join([unicode(random.randrange(10000000000)),unicode(datetime.datetime.today())])).hexdigest()
			
			lses=""
			
			if (pswd==wk.passwd):
				sessions=db.GqlQuery('SELECT * FROM Session WHERE user=:usr',usr=wk)
				m=datetime.date.today()+datetime.timedelta(days=1)
				for ss in sessions:
					if(ss.dateEnd<=datetime.date.today()):
						db.delete(ss)				
				if (self.request.get('longsess')=="True"):
					m=datetime.date.today()+datetime.timedelta(days=30)
					lses="expires=%s;"%m.strftime("%a, %d %b %Y %T GTM")
				self.response.headers.add_header('Set-Cookie',"session=%s; path=/;%s"%(sess.session,lses))
				sess.dateEnd=m
				sess.user=wk
				sess.put()

		self.redirect('/')
		
class Logout(webapp.RequestHandler):
	def get(self):
		self.response.headers.add_header('Set-Cookie',"session=; path=/;")
		self.redirect('/')
