#encoding=UTF-8
from mysql_connect import *

class Savefile(object):
    banner_td_html = ''
    port_td_html = ''
    def __init__(self,CORE):
        self.CORE =CORE

    def select_banner(self):
        sql = "select * from bannerlist"
        results = self.CORE.select(sql)
        return results

    def select_port(self):
        sql = "select * from portlist"
        results = self.CORE.select(sql)
        return results

    def save_to_file(self):
        raw_html = """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css" />
<title>Test Result</title>
</head>
<body>
<nav class="navbar navbar-default navbar-inverse" role="navigation">
  <div class="container-fluid">
 　<div class="navbar-header">
    <a class="navbar-brand" href="#">Result</a>
   </div>
      <ul class="nav navbar-nav">
    <li><a href="#port">Portlist</a></li>
    <li><a href="#banner">Bannerlist</a></li>
    </ul>
</div>
</div>
</nav>
<div class="banner_result" id="port">
<table class="table table-hover table-bordered">
   <thead>
     <tr>
        <th>Host</th><th>ServerName</th><th>Port</th>

     </tr>
   </thead>
   <tbody>
        """
        port_result=self.select_port()
        for i in range(len(port_result)):
            self.port_td_html+= "<tr>"
            for j in range(1,4):
                self.port_td_html+= "<td>"+str(port_result[i][j])+"</td>"
            self.port_td_html+= "</tr>"
        raw_html+=self.port_td_html
        raw_html+="""
</tbody>
</table>
</div>
<div class="banner_result" id ="banner">
<table class="table table-hover table-bordered">
   <thead>
     <tr>
       <th>Url</th><th>status_code</th><th>title</th><th>banner</th>
     </tr>
   </thead>
   <tbody>
    <tr>
"""
        banner_result=self.select_banner()
        for i in range(len(banner_result)):
            self.banner_td_html+="<tr>"
            for j in banner_result[i]:
                self.banner_td_html+= "<td>"+str(j)+"</td>"
            self.banner_td_html+= "</tr>"
        raw_html+=self.banner_td_html
        raw_html+="""
</tbody>
</table>
</div>
</body>
</html>
"""
        #save to file
        with open('result.html','w') as fobj:
            fobj.writelines(raw_html)
            print "file has been saved to result.html"


mysql = CORE()
