import base64
import json
import os
import re
import threading
import time
import urllib.request

import requests  # 用requests库，方便保存会话 功能和urllib差不多
from bs4 import BeautifulSoup, SoupStrainer  # 网页解析库 可以替代正则来获取你想要的内容
from PIL import Image  # 操作图片
from requests.packages import urllib3

urllib3.disable_warnings()
session = requests.Session()  # session会话对象，请求和返回的信息保存在session中
session.verify = False
def get(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
    }
    reqs = session.get(url, headers=header)
    reqs.encoding = 'UTF-8-SIG'
    if(reqs.text.find('网络可能存在问题') > -1 or reqs.text.find('您选择的日期不在预售期范围内') > -1):
        print('网络可能存在问题')
        return ''
    return reqs.text
def post(url, data):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
    }
    reqs = session.post(url, headers=header, data=data)
    reqs.encoding = 'UTF-8-SIG'
    if(reqs.text.find('网络可能存在问题') > -1 or reqs.text.find('您选择的日期不在预售期范围内') > -1):
        print('网络可能存在问题')
        return ''
    return reqs.text

# 获取二维码图片
def getQR():
    data = post(
        'https://kyfw.12306.cn/passport/web/create-qr64', {"appid": "otn"})
    json_result = json.loads(data)  # 是json格式 直接转成json方便操作
    if(json_result['result_code'] == "0"):
        uuid = json_result['uuid']
        threading._start_new_thread(checkqr,(uuid,)) # 开一个线程去执行监听

        login_pic = getImage(base64.b64decode(json_result['image']))
        Image.open(login_pic).show()  # 依赖PIL库，打开图片(会创建一个零食文件打开图片，图片未被占用时销毁)
def getImage(img):
    filepath = './login.png'
    with open(filepath, 'wb') as fd:  # w写入 b二进制形式
        fd.write(img)
    return filepath

def checkqr(uuid):
    while(True):
        checkqr_url = 'https://kyfw.12306.cn/passport/web/checkqr'
        data = post(checkqr_url, {"uuid": uuid, "appid": "otn"})
        json_result = json.loads(data)
        status_code = json_result['result_code']
        if(status_code == "1"):
            print('已扫描请确定')
        elif(status_code == "2"):
            print(json_result['result_message'])
            auth()
            return
        elif(status_code == '3'):  # 二维码过期
            getQR()
            return
        time.sleep(2)



# 检查是否登陆
def checkuser():
    url = 'https://kyfw.12306.cn/otn/login/checkUser'
    data = post(url, {"_json_att: ": ""})
    json_result = json.loads(data)
    print(json_result)

#扫码之后验证
def auth():
    try:
        data = post('https://kyfw.12306.cn/passport/web/auth/uamtk',
                    {"appid": "otn"})
        json_result = json.loads(data)
        authinfo = post('https://kyfw.12306.cn/otn/uamauthclient',
                        {"tk": json_result['newapptk']})
        json_result = json.loads(authinfo)
        if(json_result['result_code']==0):#登陆成功后保存cookie
            saveCookie() 
            print("登陆成功，用户名："+json_result["username"])
            
    except json.decoder.JSONDecodeError: # 转json失败 一般就是验证失败了 回来的一般是让你登陆的
        print('验证失败')

#保存cookie
def saveCookie():
    _cookies = session.cookies.get_dict()
    #取到session的cookie信息 取出来是键值对把他转化成字符串类型保存下来
    cookieStr = json.dumps(_cookies) 
    with open('./cookies.txt','w') as f:
        f.write(cookieStr)
        print('记录cookie成功')

#取出cookie
def getCookie():
    try:
        with open('./cookies.txt','r') as f: 
            _cookie = json.load(f)
            #session的cookie是一个RequestsCookieJar类型的，把键值对转换为给他
            session.cookies =requests.utils.cookiejar_from_dict(_cookie) 
    except FileNotFoundError: #
        print('还未登陆过..')


select_ticket_URL = 'leftTicket/queryA'  # 查票的地址是在queryA、queryZ啥的随机变化的
#查票
def select_ticket():
    train_date = TicketDTO['train_date'] # 日期
    from_station = TicketDTO['from_station']  # 起点站
    to_station = TicketDTO['to_station']  # 终点站
    global select_ticket_URL  # 查询的query后会随机变成AZ什么的
    url = 'https://kyfw.12306.cn/otn/'+select_ticket_URL +\
        '?leftTicketDTO.train_date='+train_date + \
        '&leftTicketDTO.from_station='+from_station +\
        '&leftTicketDTO.to_station='+to_station+'&purpose_codes=ADULT'  # ADULT：普通票
    data = get(url)

    json_result = json.loads(data)
    print(json_result)
    if(not json_result['status']):
        select_ticket_URL = json_result['c_url']
        select_ticket()
        return
    city_info = json_result['data']['map']  # 城市信息
    for item in json_result['data']['result']:
        classes = item.split('|') #被竖线隔开的
        canBuy = classes[11]  # 是否可购买
        secretStr = urllib.request.unquote(classes[0])  # 下单信息
        IsEnable = (classes[0] == "" and False or True)  # 有无预定信息
        TrainNum = classes[3]  # 班次
        FirstSeat = classes[31]  # 一等座
        SecondSeat = Convert(classes[30])   # 二等座
        print(canBuy+"=> 班次："+TrainNum+" 历程：" + classes[13]+" "+city_info[classes[6]]+"=>"+city_info[classes[7]] +" "+classes[8]+"-" + classes[9]+"["+classes[10] + "h] 一等座："+str(FirstSeat)+" 二等座："+str(SecondSeat))
   

def Convert(val):
    if(val == '无' or val == ''):
        return 0
    elif(val == '有'):
        return 20
    return int(val)


with open('./city.json', encoding='utf-8') as f:
    CITY_DATA = json.load(f)

TicketDTO={} # 封装请求参数
def initTicketDTO():
    TicketDTO['train_date']='2019-01-11'
    TicketDTO['from_station'] = CITY_DATA['杭州']
    TicketDTO['to_station']= CITY_DATA['重庆北']


if __name__ == "__main__":
    initTicketDTO()
    print(TicketDTO)
    select_ticket()
