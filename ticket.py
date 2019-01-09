import base64
import json
import os
import re
import time

import requests  # 用requests库，方便保存会话 功能和urllib差不多
from bs4 import BeautifulSoup, SoupStrainer  # 网页解析库 可以替代正则来获取你想要的内容
from PIL import Image  # 操作图片

import threading

session = requests.Session()  # session会话对象，请求和返回的信息保存在session中
def get(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    reqs = session.get(url, headers=header)
    return reqs.text
def post(url, data):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    reqs = session.post(url, headers=header, data=data)
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
   
def auth():
    data = post('https://kyfw.12306.cn/passport/web/auth/uamtk',
                {"appid": "otn"})
    json_result = json.loads(data)
    authinfo = post('https://kyfw.12306.cn/otn/uamauthclient',
                    {"tk": json_result['newapptk']})
    json_result = json.loads(authinfo)
    data = get('https://kyfw.12306.cn/otn/index/initMy12306Api')
    print(data)
    print('登陆成功！')
    checkuser()

if __name__ == "__main__":
    getQR()
    
