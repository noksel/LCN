# -*- coding: UTF-8 -*-


import sys
import cgi
import workers
import equipment
import PlanEq
import vendor
import payer
import wsgiref.handlers
import order
import subm
import toOrder
import lcncss
import tpay
import updateOrder
import properties
import sign
import notice
import groups
sys.path.append('/media/lnx/google_appengine')
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app



class MainPage(webapp.RequestHandler):
  def get(self):
		if(("session" in self.request.str_cookies) and (self.request.str_cookies['session']!="")):
			try:
				lwk= db.get(self.request.str_cookies['session'])
				self.response.out.write(u"""<html>
		<head>
			%s
			<script src="/script/jquery-1.5.2.min.js"></script>
			<script type="text/javascript">
				$(document).ready( function()
				{
					$('#sbBtn').click( function()
					{
						var fm= $('<form method="post" action="/notice/add">'
						+'<input name="title" value="'+$('input[name=title]')[0].value+'">'
						+'<textarea name="body" cols="100" rows="10">'+$('textarea[name=body]')[0].value +'</textarea>'
						+'</form>')
						if($('input[name=title]')[0].value=='')
							alert('Введите заголовок объявления');
						else if($('textarea[name=body]')[0].value=='')
							alert('Введите текст объявления');
						else if($('textarea[name=body]')[0].value.length>850)
							alert('Текст объявления слишком длинный');
						else
							fm.submit();
					}						
					);
				}				
				);
				
			</script>			
			</head>
		<body>
			%s"""%(lcncss.style,lcncss.beg(lwk.surname)))
			
				nts=db.GqlQuery("SELECT * FROM Notice ORDER BY date DESC")[0:4]
				
				for nt in nts:
					self.response.out.write(u"""<div class="ntRow">Автор:</div> <div class="ntD">%s</div><div class="ntRow">Дата:</div> <div class="ntD">%s</div> <div class="ntRow">Заголовок:</div> <div class="ntD">%s</div> <div class="ntRow">Объявление:</div> <div class="ntD">%s</div><hr/>"""%(nt.author.surname,nt.date,nt.title,nt.body))
			
				self.response.out.write(u"""<div><form method="post" action="/notice/add">Заголовок объявления: <input  name="title"><br/>
			Объявление:<br/> <textarea name="body" cols="100" rows="10"></textarea><br/><input id="sbBtn" type="button" value="Отправить"></form>
			 </div>""")
			
				self.response.out.write(u"""%s
		</body>
		</html>		
		"""%(lcncss.Mtempl.end))
			except (db.BadKeyError, AttributeError):
				self.redirect('/login')
			


		else:
			self.redirect('/login')
appl = webapp.WSGIApplication([('/login', sign.Login)
															,('/', MainPage)
															,('/notice/add',notice.AddNotice)
															,('/sign',sign.Sign)
															,('/logout',sign.Logout)
															,('/workers',workers.WorkersPage)
															,('/workers/workerPg',workers.WorkerPg)
															,('/workers/add',workers.AddWorker)
															,('/workers/worker/update',workers.UpdtWorker)															
															,('/worker/set-passwd-pg',workers.SetPasswdPg)
															,('/worker/set-passwd',workers.SetPasswd)
															,('/worker/gen-reset',workers.GenReset)
															,('/groups',groups.GroupsPage)
															,('/groups/add',groups.GroupAdd)
															,('/equipment',equipment.EqPage)
															,('/equipment/add',equipment.AddEq)
															,('/planeq',PlanEq.PlanEqPage)
															,('/planeq/add',PlanEq.PEAdd)
															,('/planeq/del',PlanEq.PEDel)
															,('/pgplaneqadd',PlanEq.PgPlanEqAdd)
															,('/vendor',vendor.VendorPage)
															,('/vendor/add',vendor.VendorAdd)
															,('/payer',payer.PayerPage)
															,('/payer/add',payer.PayerAdd)
															,('/order',order.OrderPage)
															,('/order/submit',subm.submEnd)
															,('/order/update-pg',updateOrder.UpdateOrderPg)
															,('/order/update',order.OrdUpdate)
															,('/order/add',order.OrdAdd)
															,('/order/dell',order.DellOrd)
															,('/order/tohist',order.OrdToHist)
															,('/planeq/to-order',toOrder.ToOrderPage)
															,('/tpaymnt',tpay.TypePayPg)
															,('/tpaymnt/add',tpay.TypePaymntAdd)],debug=True)


def init():
	eqp=equipment.Equipment(name=u'Пины HPA-OJ,SPR-OW-1')
	eqp.put()
	eqm=equipment.Equipment(name=u'Микросхемы')
	eqm.put()
	eq=equipment.Equipment(name=u'Резисторы')
	eq.put()
	eql=equipment.Equipment(name=u'ЛОВ ОВ-65')
	eql.put()
	eq=equipment.Equipment(name=u'Тележка подьёмная')
	eq.put()
	eq=equipment.Equipment(name=u'Криогенные разъемы. Micro-D connector: on sample holder wiring part it is M83513/02-DC 25 pole receptacle, socket, class M, solder type (пары) Криогенные разъемы M83513/01-DC 25 pole plug, pin, class M, solder type (пары)')
	eq.put()
	
	wk=workers.Worker(surname=u"Вдовин", name=u"Вячеслав", patronymic=u"Фёдорович", email=u'vdovin_iap@mail.ru')
	wk.put()
	wk=workers.Worker(surname=u"Кузнецов", name=u"Леонид", patronymic=u"Сергеевич")	
	wk.put()
	wk=workers.Worker(surname=u"Ширяев", name=u"Михаил", patronymic=u"Виссарионович", email=u'mv_shi@mail.ru')
	wk.put()	
	wk=workers.Worker(surname=u"Соколов")	
	wk.put()
	wkk=workers.Worker(surname=u"Коротаев")	
	wkk.put()	
	wkb=workers.Worker(surname=u"Большаков", name=u"Олег", email=u'obolshakov@mail.ru')	
	wkb.put()
	wka=workers.Worker(surname=u"Абашин", name=u"Евгений",patronymic=u"Борисович",email=u'evgbor46@mail.ru')	
	wka.put()
	wksh=workers.Worker(surname=u"Штанюк")	
	wksh.put()
	wk=workers.Worker(surname=u"Тарсов")	
	wk.put()
	wk=workers.Worker(surname=u"Елисеев")	
	wk.put()
	wk=workers.Worker(surname=u"Темнов")	
	wk.put()
	wk=workers.Worker(surname=u"Дрягин")	
	wk.put()
	wkl=workers.Worker(surname=u"Леснов", email='ss18f@mail.ru',passwd="111111" )	
	wkl.put()
	
	tpaymnt= tpay.TypePayment(name=u'Контракт')
	tpaymnt.put()
	tpaymnt= tpay.TypePayment(name=u'Котировка')
	tpaymnt.put()
	tpaymnt= tpay.TypePayment(name=u'Счёт')
	tpaymnt.put()
	tpaymnt= tpay.TypePayment(name=u'Наш долг')
	tpaymnt.put()

	
	
	pe= PlanEq.PlanEq(equipment=eqp,quantity=1,comment=u'Набор',respWk=wkk)
	pe.put()
	pe= PlanEq.PlanEq(equipment=eqm,quantity=1,comment=u'Набор',respWk =wkb)
	pe.put()
	pe= PlanEq.PlanEq(equipment=eql,quantity=1,comment=u'Набор',respWk =wka)
	pe.put()
	
	
	pr=payer.Payer(name=u'ОКБ РВТ')
	pr.put()		
	pr=payer.Payer(name=u'Гиком')
	pr.put()		
	pr=payer.Payer(name=u'ЛКН(НГТУ)')
	pr.put()
	
	
	vd=vendor.Vendor(name=u'ООО "Абтроникс"')
	vd.put()
	vd=vendor.Vendor(name=u'ООО "Миком"')
	vd.put()
	vd=vendor.Vendor(name=u'ЗАО "Радэком"')
	vd.put()
	vd=vendor.Vendor(name=u'ООО "Рубикон"')
	vd.put()
	vd=vendor.Vendor(name=u'ОКБ РВТ')
	vd.put()
	vd=vendor.Vendor(name=u'ООО "Торговый Дом Паллет Тракс"')
	vd.put()
	
	grpa=workers.Group(name=u"Администраторы")
	grpa.put()
	grpw=workers.Group(name=u"Работники")
	grpw.put()
	grp=workers.Group(name=u"Ответственные")
	grp.put()
	grp=workers.Group(name=u"Внешние службы")
	grp.put()
	grp=workers.Group(name=u"Студенты")
	grp.put()
	grp=workers.Group(name=u"Аспиранты")
	grp.put()	
	
	usr_grp = workers.UsrGroup(user=wkl,group=grpa)
	usr_grp.put()
	
def erase():
	
	eqs=db.GqlQuery('SELECT * FROM Equipment')
	db.delete(eqs)
	
	wks=db.GqlQuery('SELECT * FROM Worker')
	db.delete(wks)
	
	tps=db.GqlQuery('SELECT * FROM TypePayment')
	db.delete(tps)
	
	peqs=db.GqlQuery('SELECT * FROM PlanEq')	
	db.delete(peqs)	

	prs=db.GqlQuery('SELECT * FROM Payer')
	db.delete(prs)
	
	vds=db.GqlQuery('SELECT * FROM Vendor')	
	db.delete(vds)
	
	ords=db.GqlQuery('SELECT * FROM Order')
	db.delete(ords)
	
	ends=db.GqlQuery('SELECT * FROM Endorsment')
	db.delete(ends)
	
	prs=db.GqlQuery("select * from Property")
	db.delete(prs)
		
	usr_grp=db.GqlQuery("select * from UsrGroup")
	db.delete(usr_grp)
	
	nts=db.GqlQuery("SELECT * FROM Notice ORDER BY date DESC")
	db.delete(nts)
	
	grp=db.GqlQuery("select * from Group")
	db.delete(grp)
def main():
 wsgiref.handlers.CGIHandler().run(appl)
 #erase()
 prs=db.GqlQuery("select * from Property where name=:name",name="init")
 if (prs.count()==0 or prs[0].value=="false"):
 
 	init()
 	pr=properties.Property(name="init", value="true")
 	pr.put()
 

 
if __name__=="__main__":
	main()
