#!/usr/bin/python
# coding: utf-8

import redis
import fileinput

src_file='/Users/wukui/Downloads/taskidgroupid.csv'

def get_key(id1, id2):
    r = redis.StrictRedis(host='172.16.10.40', port=6381, password='redishtjy1', db=13)
    key='reation:guid:task:' + str(id1) + ':group:' + str(id2)
    status = r.hgetall(key)
    if status:
        print('空')
    else:
        print(status)
for i in fileinput.input(src_file):
    id=str(i)
    id1=id.split(',')[0]
    id2=id.split(',')[1]
    get_key(id1,id2)
    #break



