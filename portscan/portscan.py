#encoding=UTF-8

import datetime
import sys
import socket
import Queue
import threading
import time

#timeout
Timeout=3
#thread_num
thread_num = 20
#线程锁
lock = threading.Lock()

class ScanThread(threading.Thread):
    #多线程构造函数，传入IP地址
    def __init__(self,queue,ip):
        threading.Thread.__init__(self)
        self.queue = queue
        self.ip=ip
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
        if lock.acquire():
            try:
                #打印输出
                print '[-]%d\topen\t%s' % (port,socket.getservbyport(port))
            except:
                print '[-]%d\topen\t' % (port)
            lock.release()
        return True

    def run(self):
        while True:
            if self.queue.empty():
                break
            try:
                self.Ping(self.queue.get())
            except Exception,e:
                print e



if __name__=='__main__':
    #多线程初始化
    threads=[]
    portlist=[]
    queue=Queue.Queue()
    #提示信息
    print """
    Usage:portscan.py ip
          portscan.py ip beginport-endport
    For example:portscan.py 127.0.0.1
                portscan.py 127.0.0.1 80-10000
    """
    if len(sys.argv)==2:
        portlist=[21,22,23,25,69,80,81,82,83,84,110,389,389,443,445,488,512,513,514,873,901,1043,1080,1099,1090,
                  1158,1352,1433,1434,1521,2049,2100,2181,2375,2601,2604,3128,3306,3307,3389,4440,4444,4445,4848,
                  5000,5280,5432,5500,5632,5900,5901,5902,5903,5984,6000,6033,6082,6379,6666,7001,7001,7002,7070,
                  7101,7676,7777,7899,7988,8000,8001,8002,8003,8004,8005,8006,8007,8008,8009,8069,8080,8081,8082,
                  8083,8084,8085,8086,8087,8088,8089,8090,8091,8092,8093,8094,8095,8098,8099,8980,8990,8443,8686,
                  8787,8880,8888,9000,9001,9043,9045,9060,9080,9081,9088,9088,9090,9091,9100,9200,9300,9443,9871,
                  9999,10000,10068,10086,11211,20000,22022,22222,27017,28017,50060,50070]
    elif len(sys.argv)==3:
        try:
            inputlist=sys.argv[2].split('-')
            portlist=[i for i in range(int(inputlist[0]),int(inputlist[1])+1)]
        except:
            print "Paramater Error"
            sys.exit()
    else:
        print "Paramater Error"
        sys.exit()
    print u"当前时间:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    past=datetime.datetime.now()
    print "testing %s:" % sys.argv[1]
    for i in portlist:
        queue.put(i)
    for i in xrange(thread_num):
        threads.append(ScanThread(queue,sys.argv[1]))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    #程序时间差计算
    print u"共计用时:",datetime.datetime.now()-past
