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
import ordadd
import lcncss
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
	self.response.out.write(u"""
		<html>
		<head>
			%s
			</head>
		<body>
			%s
			<div id="centre"></div>
		</body>
		</html>

		"""%(lcncss.style,lcncss.templ))
appl = webapp.WSGIApplication([('/', MainPage)
															,('/workers',workers.WorkersPage)
															,('/workers/add',workers.AddWorker)
															,('/equipment',equipment.EqPage)
															,('/equipment/add',equipment.AddEq)
															,('/planeq',PlanEq.PlanEqPage)
															,('/planeq/add',PlanEq.PEAdd)
															,('/pgplaneqadd',PlanEq.PgPlanEqAdd)
															,('/vendor',vendor.VendorPage)
															,('/vendor/add',vendor.VendorAdd)
															,('/payer',payer.PayerPage)
															,('/payer/add',payer.PayerAdd)
															,('/order',order.OrderPage)
															,('/order/submit',subm.submEnd)
															,('/planeq/to-order',toOrder.ToOrderPage)
															,('/order/add',ordadd.Ordadd)],debug=True)


def init():

	eqs=db.GqlQuery('SELECT * FROM Equipment')
	db.delete(eqs)
	
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
	
	wks=db.GqlQuery('SELECT * FROM Worker')
	db.delete(wks)
	
 	wk=workers.Worker(surname=u"Соколов")	
	wk.put()
	wkk=workers.Worker(surname=u"Коротаев")	
	wkk.put()	
	wkb=workers.Worker(surname=u"Большаков")	
	wkb.put()
	wka=workers.Worker(surname=u"Абашин")	
	wka.put()
	wksh=workers.Worker(surname=u"Штанюк")	
	wksh.put()
	wk=workers.Worker(surname=u"Вдовин")	
	wk.put()
	
	peqs=db.GqlQuery('SELECT * FROM PlanEq')	
	db.delete(peqs)	
	pe= PlanEq.PlanEq(equipment=eqp,quantity=1,comment=u'Набор',resp=["%s"%wkk.key()])
	pe.put()
	pe= PlanEq.PlanEq(equipment=eqm,quantity=1,comment=u'Набор',resp =["%s"%wkb.key()])
	pe.put()
	pe= PlanEq.PlanEq(equipment=eql,quantity=1,comment=u'Набор',resp =["%s"%wka.key(),"%s"%wksh.key()])
	pe.put()
	
	prs=db.GqlQuery('SELECT * FROM Payer')
	db.delete(prs)
	pr=payer.Payer(name=u'ОКБ РВТ')
	pr.put()		
	pr=payer.Payer(name=u'Гиком')
	pr.put()		
	pr=payer.Payer(name=u'ЛКН(НГТУ)')
	pr.put()
	
	vds=db.GqlQuery('SELECT * FROM Vendor')	
	db.delete(vds)
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
def main():
 wsgiref.handlers.CGIHandler().run(appl)
 #init();
 
if __name__=="__main__":
	main()
