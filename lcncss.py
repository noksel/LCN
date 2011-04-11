# -*- coding: UTF-8 -*-
class Mtempl:

	end=u"""</div></div></div>"""
def beg(name):
		b1=u"""
			<div id="tble">
			<div id="caption">Заголовок</div>
			<div class="tr">
				<div id="lft">"""
		b2=u"""<input type="button" value="Выйти" onclick="javascript: window.location.href='/logout'"><br/><hr>
				<a href="/">Главная</a><br/><hr>
				<a href="/workers">Сотрудники</a><br/><hr>
				<a href="/planeq">План закупок по оборудованию</a><br/><hr>
				<a href="/order">Заявки</a><hr>
				<hr>
				<a href="/equipment">Оборудование</a><br/>
				<a href="/tpaymnt">Типы платежей</a><br/>
				<a href="/vendor">Поставщики</a><br/>
				<a href="/payer">Плательщики</a><br/>
				</div>	
				<div id="mddle">	
			"""
		return "%s%s%s"%(b1,name,b2)
def begResetPass(name):
		b1=u"""
			<div id="tble">
			<div id="caption">Заголовок</div>
			<div class="tr">
				<div id="lft">"""
		b2=u"""<br/><hr>
				<a href="/">Главная</a><br/><hr>
				<a href="/workers">Сотрудники</a><br/><hr>
				<a href="/planeq">План закупок по оборудованию</a><br/><hr>
				<a href="/order">Заявки</a><hr>
				<hr>
				<a href="/equipment">Оборудование</a><br/>
				<a href="/tpaymnt">Типы платежей</a><br/>
				<a href="/vendor">Поставщики</a><br/>
				<a href="/payer">Плательщики</a><br/>
				</div>	
				<div id="mddle">	
			"""
		return "%s%s%s"%(b1,name,b2)	
style=u"""<link rel="stylesheet" type="text/css" href="/css/lcn.css"/>"""

