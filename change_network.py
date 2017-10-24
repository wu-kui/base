#!/usr/bin/env python
# coding: utf-8

import urllib2, sys, time

username='wukui@huitongjy.com'
password='MjAxN+W5tDEw5pyIMjT'
get_token_api='http://api2.capitalonline.net/gic/v1/get_token/'
log_file = './change_network.log'




# 获取当下时间
def now():
    # 时间格式
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    return time.strftime( ISOTIMEFORMAT, time.gmtime( time.time() ))





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




#    获取虚拟数据中心的带宽信息
def get_datacenter_info(data_center_id, token):
    api = 'http://api2.capitalonline.net/gic/v1/bandwidth/public/'
    url = api + data_center_id

    http = urllib2.Request(url)
    http.add_header('token', token)
    r = urllib2.urlopen(http)

    info = r.read()
    print(info)





if __name__ == "__main__":

    status = return_token(get_token_api, username, password)
    ToKen = status['Access-Token']
    get_datacenter_info('3766742a-1243-456b-8bdc-e8b5a3b94683', ToKen)