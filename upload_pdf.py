# coding=UTF-8

pdfdir = ['/Users/wukui/test/a', '/Users/wukui/test/b', '/Users/wukui/test/c']
imgserver_url = 'http://172.16.10.29:8077/api/upload/file?fileUsageType=0'
log='log.txt'
ISOTIMEFORMAT = '%Y-%m-%d %X'   # 日志的时间格式
zip_delete_file=1               # 压缩完文件后是否删除原文件，1为删除，其它为不删除。



import sys
import os
import requests
import time
import zipfile








# 上传文件函数
def upload_imgserver(url, filename, file_size):
    '''
    用来向 imgserver 上post文件的函数
    url 为imgserver的接口url
    filename 接收上传文件的文件名
    '''
    try:
        # 上传文件
        file = {'file': open(filename, 'rb')}
        now_time = time.strftime(ISOTIMEFORMAT, time.gmtime(time.time()))
        begin_time = time.time()
        sendcode = requests.post(url, files=file)

        # 写入上传日志部分
        end_time = time.time()
        end_time = end_time - begin_time
        sendcode = sendcode.text
        sendcode = sendcode.encode("utf-8")
        sendcode = eval(sendcode)
        msg = sendcode["msg"]
        status = sendcode["status"]
        fileKey = sendcode["data"]["fileKey"]
        request_log = '\n' + str(now_time) + '   ' + filename + '   ' + msg + '    ' + str(status) + '   ' + fileKey +  '   ' + str(end_time) +  '  ' + str(file_size)
        with open(log, 'a') as f:
            f.write(request_log)

    except Exception, e:
        now_time = time.strftime(ISOTIMEFORMAT, time.gmtime(time.time()))
        e = e.message
        logs = str(now_time) + '  ' + e
        with open(log, 'a') as f:
            f.write(logs)

# upload_imgserver(imgserver_url, '/Users/wukui/test/a/1.txt',15)




# 压缩文件函数
def zip_file(filename):
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    zipfilename = filename + '.zip'
    try:
        zf = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
        zf.write(filename, basename)
    except Exception as e:
        with open(log, 'a') as f:
            f.write(e.message)
    finally:
        zf.close()
    if zip_delete_file == 1:
        os.remove(filename)

# zip_file('/Users/wukui/test/a/1.txt')




# 获取文件函数
def get_pdf_file(dir):
    '''
    先通过 zip_file 文件压缩，然后再把文件传给 upload_imgserver 函数上传。
    '''
    for dir in pdfdir:
        files = os.listdir(dir)
        for pdf in files:
            file_hz = pdf.split('.')[-1]
            file_hz.lower()
            if file_hz != 'pdf':
                continue
            filename = dir + '/' + pdf
            print filename
            zip_file(filename)
            pdf_zip = filename + '.zip'
            file_size = os.path.getsize(pdf_zip)
            upload_imgserver(imgserver_url, pdf_zip, file_size)
get_pdf_file(pdfdir)
