#encoding=utf-8
#author=Doggy
 
import os
import requests
import json
 
access_token = ''
ip_list = []
 
def login():
    user = raw_input('[-] input : username :')
    passwd = raw_input('[-] input : password :')
    print passwd
    data = {
        'username' : user,
        'password' : passwd
    }
    data_encoded = json.dumps(data)
    print data_encoded
    try:
        r = requests.post(url = 'https://api.zoomeye.org/user/login',data = data_encoded)
        r_decoded = json.loads(r.text)
        global access_token
        access_token = r_decoded['access_token']
    except Exception,e:
        print '[-] info : username or password is wrong, please try again '
        exit()
 
def saveStrToFile(file,str):
    with open(file,'w') as output:
        output.write(str)
 
def saveListToFile(file,list):
    s = '\n'.join(list)
    with open(file,'w') as output:
        output.write(s)
 
def apiTest():
    page_begin = int(raw_input("please input the page you wang to begin:"))
    page_end = int(raw_input("please input how much pages you want:"))
    page=page_begin
    global access_token
    with open('access_token.txt','r') as input:
        access_token = input.read()
    headers = {
        'Authorization' : 'JWT ' + access_token,
    }
    while(True):
        try:
            r = requests.get(url = 'https://api.zoomeye.org/host/search?query=city:nanjing+weblogic&facet=app,os&page=' + str(page),
                         headers = headers)
            r_decoded = json.loads(r.text)
            for x in r_decoded['matches']:
                print str(x['ip'])+":"+str(x['portinfo']['port'])
                ip_list.append(str(x['ip'])+":"+str(x['portinfo']['port']))
            print '[-] info : page ' + str(page)
 
        except Exception,e:
            if str(e.message) == 'matches':
                print '[-] info : account was break, excceeding the max limitations'
                break
            else:
                print  '[-] page : ' + str(e.message)
        else:
            if page == page_begin+page_end:
                break
            page += 1
 
def main():
    if not os.path.isfile('access_token.txt'):
        print '[-] info : access_token file is not exist, please login'
        login()
        saveStrToFile('access_token.txt',access_token)
    apiTest()
    saveListToFile('url.txt',ip_list)
 
if __name__ == '__main__':
    main()
