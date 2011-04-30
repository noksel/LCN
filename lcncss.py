# -*- coding: UTF-8 -*-
class Mtempl:

	end=u"""</td></tr></table>"""
def beg(name):
		b1=u"""		
			<table class="tbl"> <tr>
				<td id="lft">"""
		b2=u"""<input type="button" value="Выйти" onclick="javascript: window.location.href='/logout'"><br/><hr>
				<a class="l" href="/">Главная</a><br/><hr>
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

def begResetPass(name):
		b1=u"""
			<table class="tbl"> <tr>
				<td id="lft">"""
				
		b2=u"""<br/><hr>
				<a class="l" href="/">Главная</a><br/><hr>
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
		return "%s%s%s"%(b1,name,b2)	
style=u"""<link rel="stylesheet" type="text/css" href="/css/lcn.css"/>"""

