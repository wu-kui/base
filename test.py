#!/usr/bin/env python
# coding: utf-8

import urllib2, sys, time, json, demjson


def now():
    # 时间格式
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    return time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ))

print(now())
