#!/usr/bin/python3.7
# -- coding:utf8 --
import hashlib
import requests
import json
import configparser
import sys
s = requests.session()
c = configparser.ConfigParser()


def login(username, passwd):
    global headers
    password_md5 = hashlib.md5(passwd.encode("utf-8")).hexdigest()
    login_url = 'https://xst.nfcpwl.com/extInterface/wx/loginByStuCard'

    data = {'stuCardNo': username, 'stuCardPwd': password_md5}
    login_response = s.post(login_url, headers=headers, data=data, )
    response = {}
    z = json.loads(login_response.text)
    response['openId'] = z['mdata']['data'][0]['channelId']
    response['buyerId'] = z['mdata']['data'][0]['stuNo']
    response['customId'] = z['mdata']['data'][0]['stuNo']
    response['stuIdType'] = z['mdata']['data'][0]['stuIdType']
    openidurl = 'https://xst.nfcpwl.com/extInterface/wx/students/openId'
    openid_data = {
        'openId': response['openId'],
        'schoolNo': "3301020003"
    }
    s.post(openidurl, headers=headers, data=openid_data, )
    return response


def get_meal(user_dict):
    global headers
    data_meals = {}
    mealurl = 'https://xst.nfcpwl.com/extInterface/wx/meals'
    data_meals['customId'] = user_dict['customId']
    data_meals['openId'] = user_dict['openId']
    meal_response = s.get(mealurl, headers=headers, params=data_meals)
    mealdata = json.loads(meal_response.text)
    mealdata['openId'] = user_dict['openId']
    mealdata['customId'] = user_dict['customId']
    return mealdata


def order(orderlist):
    global text
    global is_ordered
    global days_of_week
    global mealdates
    global packagedata
    global y
    global headers
    global user_dict
    url = 'https://xst.nfcpwl.com/extInterface/wx/cart'
    cartids = [0] * days_of_week
    for j in range(days_of_week):
        if is_ordered[j]:
            continue
        data = {
            'dinnerDate': packagedata[6 * j + orderlist[j]]['PLAN_DATE'],
            'buyerId': mealdates[j]['BUYER_ID'],
            'dinnerNum': 1,
            'dinnerTime': mealdates[j]['DINNER_TIME'],
            'customId': y['customId'],
            'openId': y['openId'],
            'packageId': packagedata[6 * j + orderlist[j]]['PACKAGE_ID'],
            'price': packagedata[6 * j + orderlist[j]]['PACKAGE_PRICE'],
        }

        resp = s.post(url, headers=headers, data=data, )

        cartids[j] = json.loads(resp.text)['mdata']['data']['cartId']
    # purchase
    purchase_url = 'https://xst.nfcpwl.com/extInterface/wx/order'
    purchase_data = {
        'cartIds': cartids[:],
        'customId': y['customId'],
        'openId': y['openId'],
        'customType': user_dict['stuIdType'],
        'operationId': "100",
        'paymentStatus': '19',

    }
    purchase_resp = s.post(purchase_url, headers=headers, data=purchase_data)
    print(purchase_resp.text)


def order_rand():
    import random
    global is_ordered
    global days_of_week
    orderlist = []
    while len(orderlist) != days_of_week:
        orderlist.append(random.randint(1, 6))
    order(orderlist)


def order_code(code):
    global days_of_week
    orderlist = []

    i = 0
    while len(orderlist) != days_of_week:
        if i >= len(code):
            i = 0
        orderlist.append(ord(code[i]) - ord('A'))
        i += 1
    order(orderlist)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Referer": "https://xst.nfcpwl.com/wx/index.html",
    "Origin": "https://xst.nfcpwl.com",
    "Host": "xst.nfcpwl.com",
    "Accept": "application/json, text/plain, */*",
}
c.read(sys.path[0]+'/config.ini', encoding='UTF-8')
session = requests.session()
user_name = c.get('login', 'username')
password = c.get('login', 'password')
user_dict = login(user_name, password)
y = get_meal(user_dict)
mealdates = y['mdata']['data']['buyerList'][0]['mealDates']
packagedata = y['mdata']['data']['buyerList'][0]['packageData']
days_of_week = len(mealdates)  # 一周的点餐天数
is_ordered = [False] * days_of_week
for j in range(days_of_week):
    if mealdates[j]['ORDERED_NUM'] == 1:
        is_ordered[j] = True
if c.get('mode', 'order_mode') == 'code':
    print('按序号点餐模式')
    order_code(c.get('preferences', 'code').split())
elif c.get('mode', 'order_mode') == 'rand':
    print('随机点餐模式')
    order_rand()
