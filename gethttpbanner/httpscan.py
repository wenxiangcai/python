#!/usr/bin/env python
#coding:utf-8

import os
import re
import sys
import Queue
import threading
import optparse
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
TimeOut = 5  #request timeout
 
#User-Agent
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36','Connection':'close'}
 
class scan():
 
  def __init__(self,cidr,threads_num):
    self.threads_num = threads_num
    self.cidr = cidr
    self.IPs = Queue.Queue()
    with open(self.cidr,'r') as fobj:
      for ip in fobj:
        ip = str(ip).strip()
        self.IPs.put(ip)
 
  def request(self):
      while self.IPs.qsize() > 0:
        ip = self.IPs.get()
        try:
          r = requests.get(url="http://"+ip,headers=header,timeout=TimeOut)
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
          with open('result.txt','a') as fobj2:
            fobj2.write(" %s\t%s\t%s\t%s\n" % (str(ip),status,banner,title.decode('utf-8').encode('gbk')))
        except Exception,e:
            pass

      print '[-]testing ok!The result has been saved to result.txt'
 
  #Multi thread
  def run(self):
    for i in range(self.threads_num):
      t = threading.Thread(target=self.request)
      t.start()
 
if __name__ == "__main__":
  parser = optparse.OptionParser("Usage: %prog [options] target")
  parser.add_option("-t", "--thread", dest = "threads_num",
    default = 10, type = "int",
    help = "[optional]number of  theads,default=10")
  (options, args) = parser.parse_args()
  if len(args) < 1:
    parser.print_help()
    sys.exit(0)
  s = scan(cidr=args[0],threads_num=options.threads_num)
  s.run()
