# -*- coding: UTF-8 -*-
class Mtempl:
	beg=u"""
			<div id="tble">
			
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
	end=u"""</td></tr></table>"""
def beg(name):
		b1=u"""		
			<table class="tbl"> <tr>
				<td id="lft">"""
		b2=u"""<input type="button" value="Выйти" onclick="javascript: window.location.href='/logout'"><br/><hr>
				<a class="l" href="/workers">Сотрудники</a><br/><hr>
				<a class="l" href="/equipment">Оборудование</a><br/><hr>
				<a class="l" href="/planeq">План закупок по оборудованию</a><br/><hr>
				<a class="l" href="/order">Заявки</a><hr>
				<hr>
			
				<a class="l" href="/tpaymnt">Типы платежей</a><br/>
				<a class="l" href="/vendor">Поставщики</a><br/>
				<a class="l" href="/payer">Плательщики</a><br/>
				</td>	
				<td id="mddle">	
			"""
		return "%s<span id=\"usrN\">%s</span>%s"%(b1,name,b2)
	
style=u"""<link rel="stylesheet" type="text/css" href="/css/lcn.css"/>"""

