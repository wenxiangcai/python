#encoding=UTF-8

import datetime
import sys
import socket
import Queue
import threading
import time
from mysql_connect import *
from test_banner import *
#timeout
Timeout=3
#thread_num
thread_num = 20
#线程锁
lock = threading.Lock()

class ScanThread(threading.Thread):
    #多线程构造函数，传入IP地址
    def __init__(self,queue,ip,CORE):
        threading.Thread.__init__(self)
        self.queue = queue
        self.ip=ip
        self.CORE = CORE

    #利用ping扫描，参数是port
    def Ping(self, port):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(Timeout)
        address=(self.ip,port)
        try:
                s.connect(address)
        except:
            s.close()
            return False
        s.close()
        #线程锁
        if port == 80 or 6000<port<=9000:
            banner_list.append('http://{}:{}'.format(self.ip,port))
        elif port ==443:
            banner_list.append('https://{}:{}'.format(self.ip,port))
        if lock.acquire():
            try:
                #打印输出
                if socket.getservbyport(port):
                    print '[-]%d\topen\t%s' % (port,socket.getservbyport(port))
                    sql = "insert into portlist (host,port,server_name) values ('{}',{},'{}')".format(self.ip,port,socket.getservbyport(port))
                    self.CORE.increase(sql)
            except:
                print '[-]%d\topen\t' % (port)
                sql = "insert into portlist (host,port) values ('{}',{})".format(self.ip,port)
                self.CORE.increase(sql)
            lock.release()
        return True

    def run(self):
        while True:
            if self.queue.empty():
                break
            else:
                try:
                    self.Ping(self.queue.get(True,1))
                except Exception,e:
                    print e


        