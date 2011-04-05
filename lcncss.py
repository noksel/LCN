# -*- coding: UTF-8 -*-
class Mtempl:
	beg=u"""
			<div id="tble">
			<div id="caption">Заголовок</div>
			<div class="tr">
				<div id="lft">
				<hr>
				<a href="/workers">Сотрудники</a><br/><hr>
				<a href="/equipment">Оборудование</a><br/><hr>
				<a href="/planeq">План закупок по оборудованию</a><br/><hr>
				<a href="/order">Заявки</a><hr>
				<hr>
			
				<a href="/tpaymnt">Типы платежей</a><br/>
				<a href="/vendor">Поставщики</a><br/>
				<a href="/payer">Плательщики</a><br/>
				</div>	
				<div id="mddle">	
			"""
	end=u"""</div></div></div>"""
def bg(name):
		b1=u"""
			<div id="tble">
			<div id="caption">Заголовок</div>
			<div class="tr">
				<div id="lft">"""
		b2=u"""<br><hr>
				<a href="/workers">Сотрудники</a><br/><hr>
				<a href="/equipment">Оборудование</a><br/><hr>
				<a href="/planeq">План закупок по оборудованию</a><br/><hr>
				<a href="/order">Заявки</a><hr>
				<hr>
			
				<a href="/tpaymnt">Типы платежей</a><br/>
				<a href="/vendor">Поставщики</a><br/>
				<a href="/payer">Плательщики</a><br/>
				</div>	
				<div id="mddle">	
			"""
		return "".join([b1,name,b2])
	
style=u"""<link rel="stylesheet" type="text/css" href="/css/lcn.css"/>"""

