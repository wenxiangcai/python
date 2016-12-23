#encoding=UTF-8

from portscan import *
from test_banner import *
from save_to_html import *
def Usage():
	print """
=================================
Usage:usage.py 127.0.0.1
	  usage.py 127.0.0.1 80-10000
==================================
	"""


if __name__ == '__main__':
	threads = []
	portlist = []
	queue = Queue.Queue()
	Usage()
	#建表
	mysql = CORE()
	mysql.create_table(mysql)
	#传参
	if len(sys.argv)==2:
		portlist= [21,22,23,25,69,80,81,82,83,84,110,389,389,443,445,488,512,513,514,873,901,1043,1080,1099,1090,
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
	print "start:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	past=datetime.datetime.now()
	print "testing %s:" % sys.argv[1]
	for i in portlist:
		queue.put(i)
	for i in xrange(thread_num):
		threads.append(ScanThread(queue,sys.argv[1],mysql))
	for t in threads:
		t.start()
	for t in threads:
		t.join()
	#关闭数据库操作
	mysql.close_db()
		#程序时间差计算
	print "used:",str(datetime.datetime.now()-past)[:7]
	print "-------------------------"
	print "[-]testing  banner now..."
	banner_mysql = CORE()
	#test banner
	test = Testbanner(banner_mysql)
	print banner_list
	test.request()
	#banner output to file
	savefile_mysql = CORE()
	save = Savefile(savefile_mysql)
	save.save_to_file()
	savefile_mysql.close_db()