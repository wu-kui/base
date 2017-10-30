#!/usr/bin/env python
# coding: utf-8
# author: wukui

import urllib2, sys, time, json
import traceback, argparse

username=''
password=''
log_file = './change_network.log'







# 获取当下时间
def now():
    # 时间格式
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    return time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ))

#  记录日志的函数
def write_logs(body):
    with open(log_file, 'a') as f:
        datetime = now()
        logs = '[ ' + datetime + ' ]: ' + str(body)  + '\n'
        f.write(logs)



#   获取登陆的 ToKen 认证， 返回一个字典
def return_token(username, password):
    get_token_api = 'http://api2.capitalonline.net/gic/v1/get_token/'
    url= get_token_api
    http = urllib2.Request(url)
    http.add_header('username', username)
    http.add_header('password', password)
    r = urllib2.urlopen(http)
    status = r.read()
    status = eval(status)
    if status['status'] == "success":
        logs = '获取token成功: ' + status['status'] + ' ' + status['Access-Token']
        write_logs(logs)
        return status
    else:
        logs = '获取ToKen失败' + ' ' + str(status)
        write_logs(logs)




#    获取虚拟数据中心的带宽，直接返回带宽，单位是M。 返回一个 int
def get_datacenter_info(token, vcenter_appid):
    '''
    可以根据首都在线提供的另一个接口，来获取外网带宽。比使用现在的方法更简单。接口如下：
        http://api2.capitalonline.net/gic/v1/bandwidth/public/{public_id}
    '''
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
                logs = '没有找到带宽信息 (qos)'
                write_logs(logs)
                sys.exit(0)
    else:
        logs = '获取带宽失败:[ ' + url + ' ]'
        write_logs(logs)




#   获取虚拟数据中心的app_id，返回一个str
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
                pass
    else:
        logs = '  列虚拟数据中心失败'
        write_logs(logs)
    if not vcenter_appid:
        logs = '  没有找到该数据中心:[ ' + str(vcenter_name) + ' ]'
        write_logs(logs)
        sys.exit(1)
    return  vcenter_appid




#    获取虚拟数据中心网络的 uuid (uuid 与 public_id 是相等的)， 返回一个str
def get_network_uuid(token, vcenter_appid):
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
                uuid = net["id"]
                return uuid
            else:
                logs = '没有找到uuid'
                write_logs(logs)
                sys.exit(0)
    else:
        logs = '获取uuid失败:[ ' + url + ' ]'
        write_logs(logs)




# 更新公网带宽，需要传入 token ，public_id，更新后的带宽,返回api接口返回的信息。
def set_qos(token, public_id, qos_num, qos_old):
    api = 'http://api2.capitalonline.net/gic/v1/public/update/'
    url = api + public_id
    qos_num = int(qos_num)
    post_json = {'qos': qos_num,}
    post_json = json.dumps(post_json)
    http = urllib2.Request(url, data=post_json)
    http.add_header('token', token)
    http.add_header('Content-Type', 'application/json')
    r = urllib2.urlopen(http)

    status = r.read()
    status_dict = eval(status)

    if status_dict['status'] == 'success':
        logs = '更新带宽成功 ' + '更新后的带宽是[' + str(qos_num) + '] ' + '原来的带宽是[' + str(qos_old) + '] ' + status
        write_logs(logs)
        return status
    else:
        logs = "更新带宽失败" + status
        write_logs(logs)




if __name__ == "__main__":

    # 用于接口返回的json字串中，关键字的大小写与python不一致，需要以下处理办法
    true=True
    false=False
    none=None

    #  根据命令行给定的参数，来决定带宽大小、是否打开调度模式
    parser = argparse.ArgumentParser(description="wukui test")
    parser.add_argument('--qos_num', type=int, default=None)
    parser.add_argument('--debug', type=int, default=0)
    parser.add_argument('--vcenter', type=str, )
    args = parser.parse_args()

    qos_new = args.qos_num
    debug_mode = args.debug
    vcenter_name = args.vcenter

    #  判断给定的带宽是否符合要求
    if qos_new % 5 != 0:
        logs = '给定的带宽不是5的倍数，因为首都在线的带宽是以 5 为步长增加和减少的'
        write_logs(logs)
        if debug_mode == 1:
            print(logs)
        sys.exit(1)

    try:
        # 获取token
        status = return_token(username, password)
        ToKen = status['Access-Token']

        # 获取appid
        vcenter_appid = get_vcenter_appid(token=ToKen, vcenter_name=vcenter_name)

        # 获取带宽大小，是一个int类型
        qos_old = get_datacenter_info(ToKen, vcenter_appid)

        # 获取uuid。
        uuid = get_network_uuid(ToKen, vcenter_appid)

        # 更新带宽
        update_qos_status = set_qos(ToKen, uuid, qos_new, qos_old)

    except:
        # 把异常输出的日志文件中
        error_info = traceback.format_exc()
        if debug_mode == 1:
            print(error_info)
        write_logs(error_info)
    finally:
        # 如果是 debug模式，就输出的信息
        if debug_mode == 1:
            print("token:  " + ToKen)
            print('APPID:  ' + vcenter_appid)
            print("原来的带宽是: " + str(qos_old))
            print("新设定的带宽是: " + str(qos_new))
            print(vcenter_name + "的UUID是：" + uuid)
            print(update_qos_status)