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
