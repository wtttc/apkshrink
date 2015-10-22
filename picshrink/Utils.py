#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import shutil
import sys

__author__ = 'tiantong'


# 获取当前路径
def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


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


# 获取路径文件or文件夹大小
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


def save_dict_to_file(filePath, dict):
    try:
        output_s = open(filePath, 'w+')
        output = json.dumps(
            dict, ensure_ascii=False, indent=4, sort_keys=True)
        output_s.write(output)
        output_s.flush()
    except Exception, e:
        print e


def read_dict_from_file(filePath):
    try:
        return json.load(open(filePath))
    except Exception, ex:
        print "Error:" + str(ex)


def save_set_to_file(filePath, set):
    try:
        output_s = open(filePath, 'w+')
        output_s.writelines(["%s\n" % item for item in set])
        output_s.flush()
    except Exception, e:
        print e


def read_set_from_file(filePath):
    try:
        f = open(filePath, 'r')
        result = set()
        for line in f.readlines():
            # 去掉空白
            line = line.strip()
            # 判断是否是空行或注释行
            if not len(line) or line.startswith('#'):
                continue
            # print("line:" + line)
            result.add(line)
        return result

    except Exception, ex:
        print "Error:" + str(ex)
