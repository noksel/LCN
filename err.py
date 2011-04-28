from google.appengine.ext import webapp
import lcncss
import verify
def errPgUsr(obj,errStr):
		cUsr=verify.verifyUsr(obj)
		obj.response.out.write(u"""<html>
														<head>
														<link rel="stylesheet" type="text/css" href="/css/lcn.css"/>
														<script src="/script/jquery-1.5.2.min.js"></script>
														<script src="/script/my.js"></script>
														</head>
														<body>""")
														
		obj.response.out.write("""<div class="errNm">%s</div> """%(errStr))							
		obj.response.out.write("""</body></html>""")
