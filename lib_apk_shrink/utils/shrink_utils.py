#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import math
import shutil
import time
import functools


def open_read_file():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(file_dir):
            try:
                input_file = file(r'' + file_dir)
                f = json.load(input_file)
                input_file.close()
                return f
            except Exception, e:
                print e
                exit()

        return wrapper

    return decorator


@open_read_file()
def get_json_from_file(file_dir):
    pass


# 将bytes数据自动向上转换
def convert_bytes(bytes, lst=['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']):
    # 舍弃小数点，取小
    # 求对数(对数：若 a**b = N 则 b 叫做以 a 为底 N 的对数)
    i = int(math.floor(math.log(bytes, 1024)))

    if i >= len(lst):
        i = len(lst) - 1
    return ('%.2f' + " " + lst[i]) % (bytes / math.pow(1024, i))


def get_size_in_nice_string(sizeInBytes):
    """
    Convert the given byteCount into a string like: 9.9bytes/KB/MB/GB
    """
    for (cutoff, label) in [(1024 * 1024 * 1024, "GB"),
                            (1024 * 1024, "MB"),
                            (1024, "KB"),
                            ]:
        if sizeInBytes >= cutoff:
            return "%.1f %s" % (sizeInBytes * 1.0 / cutoff, label)

    if sizeInBytes == 1:
        return "1 byte"
    else:
        bytes = "%.1f" % (sizeInBytes or 0,)
        return (bytes[:-2] if bytes.endswith('.0') else bytes) + ' bytes'


# 获取从weibo_dev_res到根目录的路径
def get_folder_name(parent, floder_root):
    # 默认情况显示最后一个文件夹的名字
    if floder_root is not None and floder_root not in parent:
        _list = parent.split("/")
        if _list[-1].__len__() > 0:
            return _list[-1]
        return _list[-2]

    folder_name = os.path.split(parent)
    if folder_name[1] == floder_root:
        return folder_name[1]
    else:
        return get_folder_name(folder_name[0], floder_root) + os.sep + folder_name[1]


# 打印方法使用时间
def performance():
    def perf_decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kw):
            t1 = time.time()
            r = f(*args, **kw)
            t2 = time.time()
            t = (t2 - t1)
            print 'Totally used time %f s' % (t)
            return r

        return wrapper

    return perf_decorator


def get_path_size(strPath):
    if not os.path.exists(strPath):
        return 0;

    if os.path.isfile(strPath):
        return os.path.getsize(strPath);

    nTotalSize = 0;
    for strRoot, lsDir, lsFiles in os.walk(strPath):
        # get child directory size
        for strDir in lsDir:
            nTotalSize = nTotalSize + get_path_size(os.path.join(strRoot, strDir));

            # for child file size
        for strFile in lsFiles:
            nTotalSize = nTotalSize + os.path.getsize(os.path.join(strRoot, strFile));

    return nTotalSize;


def forceMergeFlatDir(srcDir, dstDir):
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    for item in os.listdir(srcDir):
        srcFile = os.path.join(srcDir, item)
        dstFile = os.path.join(dstDir, item)
        forceCopyFile(srcFile, dstFile)


def forceCopyFile(sfile, dfile):
    if os.path.isfile(sfile):
        shutil.copy2(sfile, dfile)


def isAFlatDir(sDir):
    for item in os.listdir(sDir):
        sItem = os.path.join(sDir, item)
        if os.path.isdir(sItem):
            return False
    return True


def copyTree(src, dst):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isfile(s):
            if not os.path.exists(dst):
                os.makedirs(dst)
            forceCopyFile(s, d)
        if os.path.isdir(s):
            isRecursive = not isAFlatDir(s)
            if isRecursive:
                copyTree(s, d)
            else:
                forceMergeFlatDir(s, d)
