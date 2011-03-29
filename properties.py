# -*- coding: UTF-8 -*-

from google.appengine.ext import db
from google.appengine.ext import webapp

class Property(db.Model):
	name=db.StringProperty()
	value=db.StringProperty()
