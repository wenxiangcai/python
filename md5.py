#!/usr/bin/env python
# encoding: utf-8

import json
import re
import threading
from urllib import unquote
import requests
from requests.exceptions import RequestException
import Queue

timeout = 60
retry_cnt = 2
common_headers = {u"Accept": u"text/html, application/xhtml+xml, */*", u"Accept-Encoding": u"gzip, deflate",
                  u"User-Agent": u"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                  u"Accept-Language": u"zh-CN,zh;q=0.8"}


items=[]

def cmd5(passwd):

    url = u"http://cmd5.com/"
    try_cnt = 0
    while True:
        try:
            s = requests.Session()
            req = s.get(url, headers=common_headers, timeout=timeout)
            __ = dict(re.findall(r'id="(.*?)" value="(.*?)"', req.text))

            headers = dict(common_headers, **{u"Content-Type": u"application/x-www-form-urlencoded", u"Referer": url})
            data = {u"__EVENTTARGET": __[u"__EVENTTARGET"], u"__EVENTARGUMENT": __[u"__EVENTARGUMENT"],
                    u"__VIEWSTATE": __[u"__VIEWSTATE"],
                    u"__VIEWSTATEGENERATOR": __[u"__VIEWSTATEGENERATOR"],
                    u"ctl00$ContentPlaceHolder1$TextBoxInput": passwd,
                    u"ctl00$ContentPlaceHolder1$InputHashType": u"md5",
                    u"ctl00$ContentPlaceHolder1$Button1": u'\u89e3\u5bc6',
                    u"ctl00$ContentPlaceHolder1$HiddenField1": u"",
                    u"ctl00$ContentPlaceHolder1$HiddenField2": __[u"ctl00_ContentPlaceHolder1_HiddenField2"]}
            req = s.post(url, headers=headers, data=data, timeout=timeout)
            result = re.search(r'<span id="ctl00_ContentPlaceHolder1_LabelAnswer">.+?<br(\s/)*>', req.text).group(0)
            items.append(["cmd5",re.sub(ur'(<.*?>)|(\u3002.*)', '', result)])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["cmd5","RequestError"])
                break
        except (KeyError, AttributeError), e:
            items.append(["cmd5","Error: %s" % e])
            break



def pmd5(passwd):
    url = u"http://pmd5.com/"
    try_cnt = 0
    while True:
        try:
            s = requests.Session()
            req = s.get(url, headers=common_headers, timeout=timeout)
            __ = dict(re.findall(r'id="(__VIEWSTATE|__EVENTVALIDATION)" value="(.*?)"', req.text))

            headers = dict(common_headers, **{u"Content-Type": u"application/x-www-form-urlencoded", u"Referer": url})
            data = {u"__VIEWSTATE": __[u"__VIEWSTATE"], u"__EVENTVALIDATION": __[u"__EVENTVALIDATION"], u"key": passwd,
                    u"jiemi": u"MD5\u89e3\u5bc6"}
            req = s.post(url, headers=headers, data=data, timeout=timeout)
            rsp = req.text
            if rsp.find(u"tip success") > 0:
                items.append(["pmd5",re.findall(r'<em>(.*?)</em>', rsp)[1]])
            elif rsp.find(u"tip error") > 0:
                items.append(["pmd5","NotFound"])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["pmd5","RequestError"])
                break
        except (KeyError, IndexError), e:
            items.append(["pmd5","Error: %s" % e])
            break







def navisec(passwd):
    url = u"http://md5.navisec.it/"
    try_cnt = 0
    while True:
        try:
            s = requests.Session()
            req = s.get(url, headers=common_headers, timeout=timeout)
            _token = re.search(r'name="_token" value=".+?">', req.text).group(0)[21:-2]

            headers = dict(common_headers, **{u"Content-Type": u"application/x-www-form-urlencoded", u"Referer": url})
            data = {u"_token": _token, u"hash": passwd}
            req = s.post(url + u"search", headers=headers, data=data, timeout=timeout)
            rsp = req.text
            result = re.search(r'<code>.*?</code>', rsp).group(0)[6:-7]
            num = re.search(ur'\u79ef\u5206\u5269\u4f59\uff1a([-]?\d)+', rsp).group(0)
            if result.find(u'\u672a\u80fd\u89e3\u5bc6') >= 0:
                items.append(["navisec","%s%s" % (result, num)])
            else:
                items.append(["navisec","%s %s" % (result, num)])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["navisec","RequestError"])
                break
        except AttributeError, e:
            print items.append(["navisec","Error: %s" % e])
            break


def hashtoolkit(passwd):
    url = u"http://hashtoolkit.com/reverse-hash"
    try_cnt = 0
    while True:
        try:
            params = {u"hash": passwd}
            req = requests.get(url, headers=common_headers, params=params, timeout=timeout)
            rsp = req.text
            if rsp.find(u"No hashes found for") > 0:
                items.append(["hashtoolkit","NotFound"])
            else:
                result = re.findall(r'<td class="res-text">.*?<span.*?>(.*?)</span>', rsp, re.S)[0]
                items.append(["hashtoolkit","%s" % result])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["hashtoolkit","RequestError"])
                break
        except IndexError, e:
            items.append(["hashtoolkit","Error: %s" % e])
            break


# md5-32
def md5db(passwd):
    url = u"http://md5db.net/"
    try_cnt = 0
    while True:
        try:
            req = requests.get(url + u"api/" + passwd, headers=common_headers, timeout=timeout)
            rsp = req.text
            if rsp:
                items.append(["md5db","%s" % rsp])
            else:
                items.append(["md5db","NotFound"])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["md5db","RequestError"])
                break


# md5-16, md5-32
def wmd5(passwd, action):
    url = u"http://www.wmd5.com/"
    try_cnt = 0
    while True:
        try:
            headers = dict(common_headers, **{u"Content-Type": u"application/x-www-form-urlencoded",
                                              u"X-Requested-With": u"XMLHttpRequest", u"Referer": url})
            data = {u"miwen": passwd, u"action": action}
            req = requests.post(url + u"ajax.php", headers=headers, data=data, timeout=timeout)
            rsp = req.json()
            if rsp[u"status"] == u"success":
                items.append(["wmd5","%s" % rsp.get(u"md5text", u'\u8be5\u6761\u662f\u4ed8\u8d39\u8bb0\u5f55')])
            else:
                items.append(["wmd5","NotFound"])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["wmd5","RequestError"])
                break
        except KeyError, e:
            items.append(["wmd5","Error: %s" % e])
            break


# md5-16, md5-32
def t00ls(passwd):
    url = u"https://www.t00ls.net/md5_decode.html"
    try_cnt = 0
    while True:
        try:
            s = requests.Session()
            req = s.get(url, headers=common_headers, timeout=timeout)
            formhash = re.search(r'name="formhash" value=".*?" />', req.text).group(0)[23:-4]

            headers = dict(common_headers, **{u"Content-Type": u"application/x-www-form-urlencoded",
                                              u"X-Requested-With": u"XMLHttpRequest", u"Referer": url})
            data = {u"querymd5": passwd, u"md5type": u"decode", u"formhash": formhash, u"querymd5submit": u"decode"}
            req = s.post(url, headers=headers, data=data, timeout=timeout)
            rsp = req.json()
            if rsp[u"result"] == u"error" and u'\u5df2\u67e5\u5230' not in rsp[u"msg"]:
                items.append(["t00ls","%s" % rsp[u"msg"]])
            elif rsp[u"result"] == u"success":
                items.append(["t00ls","%s" % rsp[u"mingwen"]])
            else:
                items.append(["t00ls","%s" % rsp[u"msg"]])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["t00ls","RequestError"])
                break
        except (AttributeError, KeyError), e:
            items.append(["t00ls","Error: %s" % e])
            break





def isilic(passwd):
    url = u"http://cracker.isilic.org/"
    try_cnt = 0
    while True:
        try:
            params = {u"do": u"search"}
            headers = dict(common_headers, **{u"Content-Type": u"application/x-www-form-urlencoded",
                                              u"X-Requested-With": u"XMLHttpRequest", u"Referer": url})
            data = {u"isajax": 1, u"md5": passwd}
            req = requests.post(url, params=params, headers=headers, data=data, timeout=timeout)
            req.encoding = "utf-8"
            rsp = req.text
            if rsp.find(u"oktip") > 0:
                items.append(["isilic","%s" % re.findall(r'<strong>(.*?)</strong>', rsp)[2]])
            else:
                items.append(["isilic","%s" % re.search(r'<p>.+?<a', rsp).group(0)[3:-2]])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["isilic","RequestError"])
                break
        except (AttributeError, IndexError), e:
            items.append(["isilic","Error: %s" % e])
            break


# md5-16, md5-32, sha1, mysql323, mysql5, discuz
def chamd5(passwd, type):
    url = u"http://www.chamd5.org/"
    try_cnt = 0
    while True:
        try:
            s = requests.Session()
            headers = dict(common_headers, **{u"Content-Type": u"application/json", u"Referer": url,
                                              u"X-Requested-With": u"XMLHttpRequest"})
            data = {u"email": u"akb0016@126.com", u"pass": u"!Z3jFqDKy8r6v4", u"type": u"login"}
            s.post(url + u"HttpProxyAccess.aspx/ajax_login", headers=headers, data=json.dumps(data),
                   timeout=timeout)

            data = {u"hash": passwd, u"type": type}
            req = s.post(url + u"HttpProxyAccess.aspx/ajax_me1ody", headers=headers, data=json.dumps(data),
                         timeout=timeout)
            rsp = req.json()
            result = re.sub(r'<.*?>', '', json.loads(rsp[u"d"])[u"msg"])
            if result.find(u'\u7834\u89e3\u6210\u529f') > 0:
                items.append(["chamd5","%s" % re.search(ur'\u660e\u6587:.*?\u7528\u65f6', result).group(0)[:-2].strip()])
            elif result.find(u'\u91d1\u5e01\u4e0d\u8db3') >= 0:
                items.append(["chamd5","%s" % result])
            else:
               items.append(["chamd5","NotFound"])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["chamd5","RequestError"])
                break
        except (AttributeError, ValueError), e:
            items.append(["chamd5","Error: %s" % e])
            break


def md5pass(passwd):
    url = u"http://md5pass.info/"
    try_cnt = 0
    while True:
        try:
            headers = dict(common_headers, **{u"Content-Type": u"application/x-www-form-urlencoded",
                                              u"X-Requested-With": u"XMLHttpRequest", u"Referer": url})
            data = {u"hash": passwd, u"get_pass": u"Get Pass"}
            req = requests.post(url, headers=headers, data=data, timeout=timeout)
            rsp = req.text
            if rsp.find(u"Not found!") > 0:
                items.append(["md5pass","NotFound"])
            else:
                items.append(["md5pass","%s" % re.search(r"Password - <b>.*?</b>", rsp).group(0)[14:-4]])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["md5pass","RequestError"])
                break
        except AttributeError, e:
            items.append(["md5pass","Error: %s" % e])
            break

def syue(passwd):
    url = u"http://md5.syue.com/ShowMD5Info.asp"
    try_cnt = 0
    while True:
        try:
            params = {u"GetType": u"ShowInfo", u"md5_str": passwd}
            headers = dict(common_headers, **{u"X-Requested-With": u"XMLHttpRequest", u"Referer": url})
            req = requests.get(url, params=params, headers=headers, timeout=timeout)
            req.encoding = "gb2312"
            result = re.findall(r'<span.*?>(.*?)</span>', req.text)[0]
            items.append(["syue","%s" % result.strip()])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["syue","RequestError"])
                break
        except IndexError, e:
            items.append(["syue","Error: %s" % e])
            break

def gromweb(passwd):
    url = u"http://md5.gromweb.com/"
    try_cnt = 0
    while True:
        try:
            params = {u"md5": passwd}
            req = requests.post(url, headers=common_headers, params=params, timeout=timeout)
            rsp = req.text
            if rsp.find(u"succesfully reversed") > 0:
                items.append(["gromweb","%s" % re.search(r'<em class="long-content string">.*?</em>', rsp).group(0)[32:-5]])
            else:
                items.append(["gromweb","NotFound"])
            break
        except RequestException:
            try_cnt += 1
            if try_cnt >= retry_cnt:
                items.append(["gromweb","RequestError"])
                break
        except AttributeError, e:
            items.append(["gromweb","Error: %s" % e])
            break

def crack(passwd):
        threads = [threading.Thread(target=cmd5, args=(passwd,))]
        threads.append(threading.Thread(target=pmd5, args=(passwd,)))
        threads.append(threading.Thread(target=navisec, args=(passwd,)))
        threads.append(threading.Thread(target=hashtoolkit, args=(passwd,)))
        threads.append(threading.Thread(target=md5db, args=(passwd,)))
        threads.append(threading.Thread(target=wmd5, args=(passwd,u"md5show")))
        threads.append(threading.Thread(target=t00ls, args=(passwd,)))
        threads.append(threading.Thread(target=chamd5, args=(passwd, u"md5",)))
        threads.append(threading.Thread(target=isilic, args=(passwd,)))
        threads.append(threading.Thread(target=syue, args=(passwd,)))
        threads.append(threading.Thread(target=md5pass, args=(passwd,)))
        threads.append(threading.Thread(target=gromweb, args=(passwd,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return items

