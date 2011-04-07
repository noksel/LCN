# −*− coding: UTF−8 −*−

import lcncss
import random
import verify
from google.appengine.ext import db
from google.appengine.ext import webapp

class Worker(db.Model):
 surname = db.StringProperty(multiline=False)
 patronymic=db.StringProperty()
 name = db.StringProperty(multiline=False)
 email = db.StringProperty(multiline=False)
 phone=db.StringProperty(multiline=False)
 passwd=db.StringProperty()

class ResetPasswd(db.Model):
	rkey = db.StringProperty()
	worker=db.ReferenceProperty(Worker)
	
class WorkersPage(webapp.RequestHandler):
 def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
			 
 def doSmf(self):
 	wk= db.get(self.request.str_cookies['session'])
	self.response.out.write("""<html>
														%s
														<body>%s"""%(lcncss.style,lcncss.beg(wk.surname)))
	wks=db.GqlQuery('SELECT * FROM Worker')
	self.response.out.write(u'Список сотрудников лаборатории:</br></br>')
	self.response.out.write('<table border="1">')
	self.response.out.write(u"""
														<tr><th>Фамилия</th><th>Имя</th><th>Отчество</th><th>E-mail</th><th>Телефон</th> </tr>
														""")
 
	for wk in wks:
		resetPswdButton =u"<input name=\"wk\" type=\"button\" value=\"Сбросить пароль\" onclick=\"javascript:window.location.href='/worker/gen-reset?wk=%s'\"\>"%(wk.key())
		self.response.out.write("<tr><td>%s</td><td>%s</td><td>%s</td><td><a href=\"mailto:%s\">%s</a></td><td>%s</td><td>%s</td><td>%s</td></tr>"%(wk.surname,wk.name,wk.patronymic,wk.email,wk.email,wk.phone,wk.passwd,resetPswdButton))	
			
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
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')	
	
	def doSmf(self):
		wk=Worker()
		wk.surname=self.request.get('surname')
		wk.patronymic=self.request.get('patronymic')
		wk.name=self.request.get('name')
		wk.email=self.request.get('email')
		wk.phone=self.request.get('phone')
		wk.put()
		self.redirect('/workers')

class SetPasswd(webapp.RequestHandler):
	def post(self):
		key=self.request.get('rkey')
		rsts = db.GqlQuery("SELECT * FROM ResetPasswd WHERE rkey=:rkey",rkey=key)
		rst=rsts[0]		
		wk=rst.worker
		wk.passwd=self.request.get('passwd')
		wk.put()
		db.delete(rst)
		self.redirect('/')
		
class SetPasswdPg(webapp.RequestHandler):
	def get(self):
		key=self.request.get('rkey')
		rsts = db.GqlQuery("SELECT * FROM ResetPasswd WHERE rkey=:rkey",rkey=key)
		rst=rsts[0]
		self.response.out.write(u"""<html><head>%s <script type="text/javascript">
		function setpass()
		{
			var ps = document.getElementById('pass')
			var cps= document.getElementById('confpass')
			
			if(ps.value.length>5 && ps.value==cps.value)
				{
					var fm = document.createElement("form");
					fm.action="/worker/set-passwd";
					fm.method="post";
     			var inp = document.createElement("input");     
     			inp.name='rkey';
    			inp.value='%s';
      		fm.appendChild(inp);	
      		
      		var inp = document.createElement("input");     
     			inp.name='passwd';
    			inp.value=document.getElementById('confpass').value;
      		fm.appendChild(inp);
      		
					fm.submit();	
				}		
			else {
			document.getElementById('vconf').innerHTML='введите пароль'
			}
			
		}
		function keyps()
		{
			var ps = document.getElementById('pass');
			var cps= document.getElementById('confpass');
			if(ps.value.length>5 && ps.value==cps.value)
				{
					document.getElementById('vconf').innerHTML='пароли совпадают'
				}
			else if(ps.value.length<5) {document.getElementById('vconf').innerHTML='пароль должен быть длинее 6 символов'}
			
			else
			{
				document.getElementById('vconf').innerHTML='пароли не совпадают'
			}
		}
				
		</script></head> <body>%s"""%(lcncss.style,key,lcncss.Mtempl.beg))	
		self.response.out.write(u"""<b>Ввод нового пароля:</b> %s<br/><table><tr><br/><td>Введите пароль:</td><td><input id="pass" type="password"></td></tr>"""%rst.worker.surname)
		self.response.out.write(u"""<tr><td>Подтвердите пароль:</td><td><input id="confpass" type="password" onkeyup="keyps()"></td></tr></table><div id="vconf"><br/></div>		
		 <input type="button" onclick="setpass()" value="Изменить">""")
		self.response.out.write(u"""%s</body></html>"""%lcncss.Mtempl.end)
		
class GenReset(webapp.RequestHandler):
	def get(self):
		if (verify.verifyUsr(self)):
			self.doSmf()
		else:
			self.redirect('/')
	
	def doSmf(self):
		wk=db.get(self.request.get('wk'))		
		rs=ResetPasswd(rkey=str(random.randrange(1000)), worker=wk)
		self.response.out.write(u"""<html><body>Для задания пароля для "%s" перейдите по следующей ссылке:<br/><a href=\"/worker/set-passwd-pg?rkey=%s\">/worker/set-passwd-pg?rkey=%s<a></body></html>"""%(wk.surname,rs.rkey,rs.rkey))
		rs.put()
