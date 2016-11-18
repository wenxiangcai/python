#encoding=UTF-8
import bs4
import requests
import re
import urlparse
import Queue
import sys
import os
import urllib
sys.setrecursionlimit(1000000) #设置递归深度
alt_list=[]
href_list=[]

img_queue=Queue.Queue()
class Spider(object):
    def __init__(self,page):
        self.url="http://mzitu.com"
        self.queue=Queue.Queue()
        self._imagepage=1#初始页号设为1
        self._headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        if not page:
            self.page=1
        else:
            self.page=page

    def visit_page(self):
        #默认访问10页
        while self.page<2:
            url=self.url+"/page/"+str(self.page)
            self.queue.put(url)
            self.page+=1

    def get_imgurl(self):
        self.visit_page()
        #队列非空，取出元素
        while not self.queue.empty():
            pageurl=self.queue.get()
            try:
                r=requests.get(url=pageurl)
                soup=bs4.BeautifulSoup(r.text,'lxml')
                #获取img的alt标签
                getalt=soup.select('.lazy')
                for i in getalt:
                    #get href->add to href_list
                    href_list.append(i['data-original'])
            except:
                pass
        #队列取完，访问列表
        self.get_realimgurl()

    def get_realimgurl(self):
        if href_list!=[]:
            for eachimg_url in href_list:
                img_num=urlparse.urlparse(eachimg_url).path.split('/')[4][:5]
                img_queue.put(img_num)
        #载入队列完毕,访问图片链接
        while not img_queue.empty():
            img_num=img_queue.get()
            image_url="http://mzitu.com/{}/".format(img_num)
            self.visit_realimgurl(image_url,self._imagepage)

    def visit_realimgurl(self,image_url,page):
        #队列非空，取出元素
        if page==1:
            url=image_url+str(page)
            self.re_urlimg(image_url,page)
            page+=1
            self.visit_realimgurl(image_url,page)

        else:
            #递归访问page
            url=image_url+str(page)
            if(self.re_urlimg(image_url,page)):
                page+=1
                self.visit_realimgurl(image_url,page)


    def re_urlimg(self,url,page):
        #正则匹配图片链接
        try:
            r=requests.get(url=url+str(page),headers=self._headers)
            #判断页数是否到了最后
            if(self.judge_if_301(url,page)=='same') and page!=1:
                return False
            elif page==1:
            #页数为1，单独存储
                pattern=re.compile('<img src="(.*?)".*?>',re.S)
                item=re.findall(pattern,r.content)[0]
                self.save_into_file(url,page,item)
                return True
            #其他情况
            else:
                pattern=re.compile('<img src="(.*?)".*?>',re.S)
                item=re.findall(pattern,r.content)[0]
                self.save_into_file(url,page,item)
                return True
        except:
            pass

    def judge_if_301(self,url,page):
        base_page=requests.get(url+str(1)).content
        now_page=requests.get(url+str(page)).content
        if now_page==base_page:
            return "same"

    def save_into_file(self,url,page,imgurl):
        #建立文件夹
        try:
            if(os.path.exists('F:/meitu/{}/'.format(url[-6:-1]))):
                    pass
            else:
                os.makedirs('F:/meitu/{}/'.format(url[-6:-1]))
        except Exception,e:
            print e
        try:
        #保存文件
            urllib.urlretrieve(imgurl,filename='F:/meitu/{}/{}.jpg'.format(url[-6:-1],page))
            print '[-]{}/{}.jpg save success'.format(url[-6:-1],page)
        except:
            print 'file save error'
            pass


spider=Spider(1)
spider.get_imgurl()
