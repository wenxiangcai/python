#encoding=UTF-8

import requests
import sys
import re
import json


def judge(ip):
    pattern=re.compile("\d+\.\d+\.\d+\.\d+",re.S)
    items=re.findall(pattern,ip)
    if items!=[]:
        print "[-]testing %s" % (ip)
    else:
        print "IP Input Error"
        sys.exit()
        
def get_gpsinfo():
        r=requests.get(url=url,headers=headers)
        reply = json.loads(r.text)
        error=reply["result"]["error"]
        if error==161:
            print reply['content']
            if reply['content']["location_description"]:
                address = reply['content']["location_description"]
                print u'该IP的地址为：',address
            if reply['content']['address_component']['admin_area_code']:
                IDcard = reply['content']['address_component']['admin_area_code']
                print u'该地区身份证前6位：'+str(IDcard)
        else:
            print error_list[error]

if __name__=='__main__':
    print """
    Usage:test.py remote_ip pc/mb
    for example:test.py 58.123.123.123 pc
    """
    #judge paramater
    if len(sys.argv)!=3:
        print "paramater error"
        sys.exit()
    judge(sys.argv[1])
    #myak
    AK='YIogecncCOvlq2oGgWqnYRUCWhKma8dY'
    #request url
    url="http://api.map.baidu.com/highacciploc/v1?qcip=%s&qterm=%s&ak=%s&coord=bd09ll&extensions=3" % (sys.argv[1],sys.argv[2],AK)
    #headers
    headers={'Uer-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    #error handle
    error_list = {
    1:u'服务器内部错误',
    167:u'定位失败',
    101:u'AK参数不存在',
    200:u'应用不存在，AK有误请检查重试',
    201:u'应用被用户自己禁止',
    202:u'应用被管理员删除',
    203:u'应用类型错误',
    210:u'应用IP校验失败',
    211:u'应用SN校验失败',
    220:u'应用Refer检验失败',
    240:u'应用服务被禁用',
    251:u'用户被自己删除',
    252:u'用户被管理员删除',
    260:u'服务不存在',
    261:u'服务被禁用',
    301:u'永久配额超限，禁止访问',
    302:u'当天配额超限，禁止访问',
    401:u'当前并发超限，限制访问',
    402:u'当前并发和总并发超限'
    }
    #getipinfo
    get_gpsinfo()
