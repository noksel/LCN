# -*- coding: UTF-8 -*-
from google.appengine.ext import db
import workers

def verifyUsr(obj):
	if(("session" in obj.request.str_cookies) and (obj.request.str_cookies['session']!="")):
		try:
			wk= db.get(obj.request.str_cookies['session'])
			"%s"%wk.surname
			return 1;
		except:
			return 0;
	else:
		return 0;
		
def verifyRightEndors(obj,endrsment):

	if(("session" in obj.request.str_cookies) and (obj.request.str_cookies['session']!="")):
		try:
			wk= db.get(obj.request.str_cookies['session'])
			"%s"%wk.surname		
			if(endrsment.submiter.key()==wk.key()):
				return 1;
			else:
				return 0;
		except:
			return 0;
	
	else:
		return 0;
		
def getList(grp_names): #лист имён групп. возвращается list ключей сотрудников
	lst=[]
	for gr_name in grp_names:
		gr=db.GqlQuery("SELECT * FROM Group WHERE name=:nm",nm=gr_name)[0]
		usr_grps=db.GqlQuery("select * from UsrGroup where group=:grp",grp=gr)
		
		lst.extend([u'%s'%u_g.user.key() for u_g in usr_grps])
	return lst	
		
		
		
		
		
		
		
		
		
