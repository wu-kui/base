#!/usr/bin/env python
# coding: utf-8

import urllib2, sys, time, json

username='user'
password='password'
get_token_api='http://api2.capitalonline.net/gic/v1/get_token/'
log_file = './change_network.log'




# 获取当下时间
def now():
    # 时间格式
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    return time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ))





#   获取登陆的 ToKen 认证
def return_token(url, username, password):
    http = urllib2.Request(url)
    http.add_header('username', username)
    http.add_header('password', password)
    r = urllib2.urlopen(http)
    status = r.read()
    status = eval(status)
    if status['status'] == "success":
        with open(log_file, 'a') as f:
            datetime = now()
            logs = '[ ' + datetime + ' ]' + ' ' + status['status'] + ' ' + status['Access-Token'] + '\n'
            f.write(logs)
        return status
    else:
        with open(log_file, 'a') as f:
            datetime = now()
            logs = '[ ' + datetime + ' ]' + ' ' + '获取ToKen失败' + ' ' + str(status) + '\n'
            f.write(logs)




#    获取虚拟数据中心的带宽，直接返回带宽，单位是M
def get_datacenter_info(token, vcenter_appid):
    api = 'http://api2.capitalonline.net/gic/v1/app/info/'
    url = api + '?app_id=' + vcenter_appid

    http = urllib2.Request(url)
    http.add_header('token', token)
    r = urllib2.urlopen(http)
    info = r.read()
    info = eval(info)

    if info["status"] == "success":
        alldata = dict(info["data"][0])
        alldata = alldata['net']
        for net in alldata:
            if net["type"] and net["type"] == "public":
                qos = net["qos"]
                return qos
            else:
                with open(log_file, 'a') as f:
                    datetime = now()
                    logs = '[ ' + datetime + ' ]' + ' ' + '没有找到带宽信息 (qos)' + '\n'
                    f.write(logs)
                sys.exit(0)
    else:
        with open(log_file, 'a') as f:
            datetime = now()
            logs = '[ ' + datetime + ' ]' + ' ' + '获取带宽失败:[ ' + url + ' ]' + '\n'
            f.write(logs)




#   获取虚拟数据中心的app_id
def get_vcenter_appid(token,vcenter_name):
    api = 'http://api2.capitalonline.net/gic/v1/app/list/'
    url = api

    http = urllib2.Request(url)
    http.add_header('token', token)
    r = urllib2.urlopen(http)
    vcenter_info = r.read()
    vcenter_info = eval(vcenter_info)

    if vcenter_info["status"] == "success":
        for vcenter in vcenter_info["data"]:
            if vcenter["name"] == vcenter_name:
                vcenter_appid = vcenter["app_id"]
                break
            else:
                continue
    else:
        with open(log_file, 'a') as f:
            datetime = now()
            logs = '[ ' + datetime + ' ]' + ' ' + '	列虚拟数据中心失败' + ' ' + '\n'
            f.write(logs)
    if not vcenter_appid:
        with open(log_file, 'a') as f:
            datetime = now()
            logs = '[ ' + datetime + ' ]' + ' ' + '	没有找到该数据中心:[ ' + str(vcenter_name) + ' ]' + '\n'
            f.write(logs)
        sys.exit(1)
    return  vcenter_appid





if __name__ == "__main__":

    # 用于接口返回的json字串中，关键字的大小写与python不一致，需要以下处理办法
    true=True
    false=False
    none=None

    status = return_token(get_token_api, username, password)
    ToKen = status['Access-Token']
    print ToKen
    vcenter_appid = get_vcenter_appid(token=ToKen, vcenter_name='ht')
    print vcenter_appid
    dk = get_datacenter_info(ToKen, vcenter_appid)
    print dk