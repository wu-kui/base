# coding: utf-8

zip_delete_file=1


import zipfile
import os
import sys
import time



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



def is_old_file(file_name, expire):
    '''
        返回文件是否满足过期时间  0 为满足    1 为不满足
    '''
    create_date = os.path.getctime(file_name)
    now_date = time.time()
    file_expire = ( now_date - create_date ) / 60 / 60 /24
    if expire > file_expire:
        return 0
    else:
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请输入文件名")
        sys.exit(1)
    elif len(sys.argv) > 3:
        print("输入了过多的参数，只需要输入文件和和文件的过期时间就可以")
        sys.exit(2)
    file_name = sys.argv[1]
    expire = int(sys.argv[2])
    status = is_old_file(file_name, expire)
    if os.path.isfile(file_name):
        if status == 0:
            zip_file(file_name)
        else:
            print("文件不在指定的日期")
            sys.exit(3)
    else:
        print("输入不是一个正常的文件")
        sys.exit(4)