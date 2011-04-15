# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import workers

class MyExc(Exception):
	pass
		

def verifyUsr(obj):
	if(("session" in obj.request.str_cookies) and (obj.request.str_cookies['session']!="")):
		try:
			sess=db.GqlQuery('SELECT * FROM Session WHERE session=:ss',ss=obj.request.str_cookies['session'])
			if(sess.count()>0):
				return sess[0].user
			else:
				raise MyExc
		except (MyExc):
			return None
	else:
		return None

def verifyRightEndors(cUsr,endrsment):
	if(endrsment.submiter.key()==cUsr.key()):
		return 1
	else:
		return 0

		
def getList(grp_names): #лист имён групп. возвращается list ключей сотрудников
	lst=[]
	for gr_name in grp_names:
		gr=db.GqlQuery("SELECT * FROM Group WHERE name=:nm",nm=gr_name)[0]
		usr_grps=db.GqlQuery("select * from UsrGroup where group=:grp",grp=gr)
		
		lst.extend([u'%s'%u_g.user.key() for u_g in usr_grps])
	return lst	
		
		
		
		
		
		
		
		
		
