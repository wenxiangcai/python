#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import argparse
import requests
import threading
import Queue
from termcolor import colored

#introduct
text='''
--------------------------------------------------------------------
                           Webscanner    1.0
                            Writer:   Doggy
                            Mail: 1129061128@qq.com
--------------------------------------------------------------------
'''
print colored(text,'cyan')


parse=argparse.ArgumentParser()
parse.add_argument('-w','--website',help='Website Like http://www.baidu.com | www.baidu.com',type=str)
args=parse.parse_args()
print colored('Begin to scan '+args.website+'\n','magenta')

#check the website you input
website=args.website
pattern=re.compile(r'http\:\/\/|https\:\/\/')
res=re.match(pattern,website)
if not(res):
    website='http://'+website

#get string from file
dict=[]
with open('D://dict.txt') as fobj:
    while True:
        data=fobj.readline().strip()
        if len(data)==0:
            break
        geturl=website+data
        dict.append(geturl)

#write headers
headers={
    'Accept': '*/*',
    'Referer': website,
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
    'Cache-Control': 'no-cache',
}

#get wrong_url texts
error_url=website+'doggyisagoodman.html'
error_response=requests.get(error_url,headers=headers)
error_text=error_response.text


#visit url
for url in dict:
    try:
        response=requests.get(url,headers=headers)
    except Exception,e:
        print 'get url Error',e

    if (response.status_code==200 or response.status_code==302 and response.text!=error_text):
        print '[status]:'+str(response.status_code)+'\t',
        print colored(url+' exists','green')

print colored('the scan ends...','yellow')


#trying to change to multithreading....



