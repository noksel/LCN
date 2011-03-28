#-*-coding UTF-8 -*-

getChList="""function getList(chName)
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
		};"""
		
host="""host='http://localhost:8080';"""
