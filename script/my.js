function getList(chName)
		 {
		 	cht=document.getElementsByName(chName)
			 astr='';
		 	for(var i=0;i<cht.length;i++)
		 	{
				
				if (cht[i].checked)
				 {
				  if(astr=='')
				 		astr=cht[i].value
				 	else
				 		astr=astr+':'+cht[i].value
				 }
			}
			return astr;
		};
function checkCount(nm)
		{
			chk=$('input[name='+nm+']');
			for(i=0;i<chk.length;i++)
				{
					if(chk[i].checked)
						return true;
				}
				return false;
		}			
		
function checkmail(value) {
reg = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
if (!value.match(reg)) {alert("Пожалуйста, введите свой настоящий e-mail"); 
 return false; } return true;}
