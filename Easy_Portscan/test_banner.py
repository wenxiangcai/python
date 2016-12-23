#encodig=UTF-8
import re
import Queue
import requests
import threading

#banner list
banner_list = []
#User-Agent
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36','Connection':'close'}
#Time_out = 5
TimeOut = 5
class Testbanner():
    def __init__(self,CORE):
        self.IPs = Queue.Queue()
        self.CORE = CORE
        self.threads_num = 20

        for each_ip in banner_list:
            self.IPs.put(each_ip)

    def Request(self):
        while self.IPs.qsize() > 0:
            ip = self.IPs.get()
            try:
                r = requests.get(url=ip,headers=header,timeout=TimeOut)
                print '[-]testing: '+r.url
                status = r.status_code
                title = re.findall('<title>(.*)</title>', r.content) #get the title
                if title:
                    title=title[0].strip()
                else:
                    title = "None"
                banner = ''
                try:
                    banner += r.headers['Server'][:20] #get the server banner
                except:
                    banner="NULL"
            #save result
                print " {}\t{}\t{}\t{}\n".format(str(ip),status,banner,title[:10])
                sql = "insert into bannerlist (url,status_code,banner,title) values ('{}',{},'{}','{}')".format(str(ip),status,banner,title[:20])
                self.CORE.increase(sql)
            except:
                pass
        else:
            print '[-]testing ok!'

        def run(self):
            while True:
                if self.queue.empty():
                    break
                else:
                    try:
                        self.Ping(self.Re.get(True,1))
                    except Exception,e:
                        print e

