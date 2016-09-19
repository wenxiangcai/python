# coding: utf-8
import requests
import re
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#爱站whois
def aizhanwhois(domain):
    try:
        items=[]
        url="http://whois.aizhan.com/"+domain+"/"
        headers={"User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"}
        r=requests.get(url,headers=headers)
        pattern=re.compile('<td>.*?<a target="_blank" href="/reverse-whois\?q=(.*?)&t=registrant">.*?</a>',re.S)
        whois=re.findall(pattern,r.content)
        pattern2=re.compile('机构邮箱.*?<a target="_blank" href="(.*?)">.*?<img',re.S)
        email_url=re.findall(pattern2,r.content)
        if whois==[]:
            items.append('NULL')
        else:
            items.append(whois[0].strip())
        r2=requests.get(url="http://whois.aizhan.com"+email_url[0],headers=headers)
        pattern3=re.compile('<input type="text" name="q" .*?value="(.*?)" />',re.S)
        real_email=re.findall(pattern3,r2.content)
        if real_email==[]:
            items.append('NULL')
        else:
            items.append(real_email[0])
        pattern4=re.compile('Admin Phone: </b>(.*?)<br/>',re.S)
        phone=re.findall(pattern4,r.content)
        if phone==[]:
            items.append('NULL')
        else:
            items.append(phone[0])
        pattern5=re.compile('Name Server: </b>(.*?)<br/>',re.S)
        nameserver=re.findall(pattern5,r.content)
        items.append(nameserver)
        items.append("aizhan")
        items.append(email_url[0])
        return items
    except:
        pass


#站长之家whois
def zzzjwhois(domain):
    url="http://whois.chinaz.com/reverse?host="+domain+"&ddlSearchMode=0"
    headers={"User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"}
    try:
        items=[]
        r=requests.get(url=url,headers=headers)
        pattern=re.compile('<a href="\?host=.*?>(.*?)</a></div>.*?<div class="w280"><a href="\?host=.*?>(.*?)</a>',re.S)
        result=re.findall(pattern,r.content)
        if result==[]:
            items.append('NULL')
            items.append('NULL')
        else:
            items.append(result[0][0])
            items.append(result[0][1])
        items.append('NULL')
        r2=requests.get("http://whois.chinaz.com/"+domain,headers=headers)
        pattern=re.compile('<div class="fr WhLeList-right">(.*?)</div>',re.S)
        result2=re.findall(pattern,r2.content)
        if result2[-1]==[]:
            items.append('NULL')
        else:
            items.append(result2[-1].split('<br/>'))
        items.append("chinaz")
        return items
    except:
        pass

def getreversewhois(domain):
    try:
        list1=aizhanwhois(domain)
        list2=zzzjwhois(domain)
        #根据注册人查询
        results=[]
        headers={"User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"}
        url="http://whois.aizhan.com/reverse-whois?q="+list1[0]+"&t=registrant"
        r=requests.get(url=url,headers=headers)
        if r.status_code==200 or r.status_code==302:
            pattern=re.compile('<td>\d+</td>.*?<td><a.*?>(.*?)</a></td>.*?<td><a.*?>(.*?)</a></td>.*?<td><a href="(.*?)">',re.S)
            names=re.findall(pattern,r.content)
            if names==[]:
                results.append(['NULL','NULL','NULL'])
            else:
                for name in names:
                    url="http://whois.aizhan.com"+name[2]
                    r=requests.get(url=url,headers=headers)
                    pattern2=re.compile('<input type="text" name="q" .*?value="(.*?)" />',re.S)
                    real_email=re.findall(pattern2,r.content)
                    if real_email==[]:
                        results.append(['NULL','NULL','NULL'])
                    else:
                        result=[name[0].strip(),name[1].strip(),real_email[0]]
                        results.append(result)
        else:
            results.append(['NULL','NULL','NULL'])
       #根据邮箱反查
        url2="http://whois.aizhan.com"+list1[5]
        r=requests.get(url=url2,headers=headers)
        if r.status_code==200 or r.status_code==302:
            pattern=re.compile('<td>\d+</td>.*?<td><a.*?>(.*?)</a></td>.*?<td><a.*?>(.*?)</a></td>.*?<td><a href="(.*?)">',re.S)
            pattern2=re.compile('<input type="text" name="q" .*?value="(.*?)" />',re.S)
            real_email=re.findall(pattern2,r.content)
            items=re.findall(pattern,r.content)
            if real_email==[] or items==[]:
                results.append(['NULL','NULL','NULL'])
            else:
                for item in items:
                    result=[item[0].strip(),item[1].strip(),real_email[0]]
                    results.append(result)
        else:
             results.append(['NULL','NULL','NULL'])
        results.append(list1)
        results.append(list2)
        return results

    except:
        pass

