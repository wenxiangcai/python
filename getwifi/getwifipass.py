# -*- coding: utf-8 -*-
#author=Doggy
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getwifipass():
    #获取wifi名称
    instruction='netsh wlan show profiles'
    r=os.popen(instruction)
    info=r.readlines()
    print "正在获取连接过得wifi列表:"
    for eachline in info:
        #匹配规则
        pattern=u'所有用户配置文件 :(.*?)\n'
        items=re.findall(pattern,eachline.decode('gbk'))
        if items!=[]:
            #打印输出
            print "="*30
            print '[-]Wifiame: '+items[0]
            with open('wifilist.txt','a') as fobj:
                fobj.write('='*30+"\n")
                fobj.write('[-]Wifiame: '+items[0]+"\n")
            getpass='netsh wlan show profiles name=%s key=clear' % items[0].strip().encode('gbk')
            r=os.popen(getpass)
            passinfo=r.readlines()
            try:
                for eachline in passinfo:
                    pattern=u'关键内容            :(.*?)\n'
                    items=re.findall(pattern,eachline.decode('gbk'))
                    if items!=[]:
                        with open('wifilist.txt','a') as fobj:
                            fobj.write('[-]WifiPass'+items[0]+"\n")
                        print 'WifiPass:'+items[0]
                    else:
                        pass
            except:
                pass

        else:
            pass
getwifipass()


