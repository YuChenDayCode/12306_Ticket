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
    if json_result['status']:
        return json_result['data']['flag']
    return False

#扫码之后验证
def auth():
    try:
        getCookie()

        data = post('https://kyfw.12306.cn/passport/web/auth/uamtk',
                    {"appid": "otn"})
        json_result = json.loads(data)
        if(json_result['result_code']==1):
            getQR()
            auth()
            return
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
    initTicketDTO()
    global select_ticket_URL  # 查询的query后会随机变成AZ什么的
    url = 'https://kyfw.12306.cn/otn/'+select_ticket_URL +\
        '?leftTicketDTO.train_date='+TicketDTO['train_date'] + \
        '&leftTicketDTO.from_station='+ TicketDTO['from_station'] +\
        '&leftTicketDTO.to_station='+TicketDTO['to_station'] +'&purpose_codes=ADULT'  # ADULT：普通票
    data = get(url)

    json_result = json.loads(data)
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
        #print(canBuy+"=> 班次："+TrainNum+" 历程：" + classes[13]+" "+city_info[classes[6]]+"=>"+city_info[classes[7]] +" "+classes[8]+"-" + classes[9]+"["+classes[10] + "h] 一等座："+str(FirstSeat)+" 二等座："+str(SecondSeat))
        if(TrainNum in TicketDTO['class']):
            print(TrainNum+"：二等座余票："+str(SecondSeat))
            if(IsEnable and canBuy == 'Y'):  # 有提交信息 并且可以购买
                print('检测到余票，正在提交')
                if(SecondSeat > 0):
                    submitOrderRequest(secretStr)


# 检测是否有未完成的订单
def submitOrderRequest(secretStr):
    if(checkuser()):  # 下单前需要先检查登陆
        reqdata = {
            "secretStr": secretStr,
            "train_date": TicketDTO['train_date'],
            "back_train_date": time.strftime('%Y-%m-%d', time.localtime(time.time())),
            "tour_flag": 'dc',
            "purpose_codes": 'ADULT',
            "query_from_station_name": TicketDTO['from_station_name'],
            "query_to_station_name": TicketDTO['to_station_name'],
            "undefined": ''
        }
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = post(url, reqdata)
        json_result = json.loads(data)
        if(json_result['data'] == 'N' and json_result['status']):  # 无未完成的订单
            getPassenge()
        else:
            print('有未完成订单')

# 获取购票人
def getPassenge():
    html_data = post('https://kyfw.12306.cn/otn/confirmPassenger/initDc',
                     {"_json_att: ": ""})  # 点预定的时候需要先初始化一下 获取token 用于获取购票人
    REPEAT_SUBMIT_TOKEN = re.findall(re.compile(
        "var globalRepeatSubmitToken = '(.*?)';", re.S), html_data)
    key_check_isChange=re.findall(re.compile(
        "'key_check_isChange':'(.*?)',", re.S), html_data)
    leftTicketStr =re.findall(re.compile(
        "'leftTicketStr':'(.*?)',", re.S), html_data)
    json_initDc ={
        'REPEAT_SUBMIT_TOKEN':REPEAT_SUBMIT_TOKEN,
        'key_check_isChange':key_check_isChange,
        'leftTicketStr':leftTicketStr
    }

    url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    reqdata = {
        "_json_att: ": "",
        "REPEAT_SUBMIT_TOKEN": REPEAT_SUBMIT_TOKEN[0]
    }
    data = post(url, reqdata)
    json_result = json.loads(data)
    print("购票人数据：")
    for item in json_result['data']['normal_passengers']:
        print(item)


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
    TicketDTO['train_date']='2019-02-10'
    TicketDTO['from_station_name']='重庆'
    TicketDTO['to_station_name']='潼南'
    TicketDTO['class']=['D5147']
    TicketDTO['passenger'] =['']
    
    TicketDTO['from_station'] = CITY_DATA[TicketDTO['from_station_name']]
    TicketDTO['to_station']= CITY_DATA[TicketDTO['to_station_name']]
   
if __name__ == "__main__":
    auth()
    select_ticket()
'''
    getPassenge()


    initTicketDTO()
    print(TicketDTO)
    select_ticket()
'''
