# -*- coding: UTF-8 -*-
import sys
import cgi
import workers
import wadd
import equipment
import PlanEq
import PlanEqAdd
import pgplaneqadd
import vendor
import payer
import wsgiref.handlers
import order
import subm
import toOrder
import ordadd
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
	self.response.out.write(u"""
		<html>
		<body>
			<a href="workers">Сотрудники</a></br>
			<a href="equipment">Оборудование</a></br>
			<a href="planeq">План закупок по оборудованию</a></br>
			<a href="order">Заявки</a>
		</body>
		</html>

		""")
appl = webapp.WSGIApplication([('/', MainPage)
															,('/workers',workers.WorkersPage)
															,('/workers/add',wadd.AddWorker)
															,('/equipment',equipment.EqPage)
															,('/planeq',PlanEq.PlanEqPage)
															,('/planeq/planeqadd',PlanEqAdd.PEAdd)
															,('/pgplaneqadd',pgplaneqadd.PgPlanEqAdd)
															,('/vendor',vendor.VendorPage)
															,('/payer',payer.PayerPage)
															,('/order',order.OrderPage)
															,('/order/submit',subm.submEnd)
															,('/planeq/to-order',toOrder.ToOrderPage)
															,('/order/add',ordadd.Ordadd)],debug=True)

def main():
 wsgiref.handlers.CGIHandler().run(appl)
 
if __name__=="__main__":
	main()
