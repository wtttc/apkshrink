#! /usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import os
import sys
import shutil

import MakeResPicDict

__author__ = 'tiantong'

RES_NAME = "res" + os.path.sep

# BatchShrink [file path]
class BatchShrink(object):
    def __init__(self, command):
        self.command = command

    def compress(self, floder_string):
        command = self.command + " " + floder_string
        old_size = get_path_size(floder_string);
        os.popen(command).read()
        new_size = get_path_size(floder_string);
        chg_size = long(old_size) - long(new_size)
        return chg_size;


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


def compress_diff_file(res_floder, tool, old_dict_file, out_floder=None):
    tool = BatchShrink(tool)
    old_dict = MakeResPicDict.read_dict_from_file(old_dict_file)

    temp_dict = cur_file_dir() + os.path.sep + "temp_dict.txt"
    if out_floder is not None:
        temp_dict = out_floder + os.path.sep + "temp_dict.txt"

    MakeResPicDict.make_res_pic_dict(res_floder, temp_dict)
    new_dict = MakeResPicDict.read_dict_from_file(temp_dict)

    # 对比检查出新修改的文件
    file_to_compress = set()

    for k, v in new_dict.items():
        if k in old_dict:
            if old_dict[k] != new_dict[k]:
                # changed
                file_to_compress.add(k)
        else:
            # new
            file_to_compress.add(k)

    print("file_to_compress:" + str(file_to_compress))

    output_dir = os.path.join(cur_file_dir(), "temp")
    # 保证temp存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历复制修改的文件到temp
    for parent, dirnames, filenames in os.walk(res_floder):
        for d in dirnames:
            if "drawable" not in str(d):
                continue
            for sp, sd, sf in os.walk(os.path.join(parent, d)):
                for ssf in sf:
                    file_path = os.path.join(sp, ssf)
                    dict_key_index = file_path.find(RES_NAME)
                    dict_key = file_path[dict_key_index:]
                    # print("key:" + str(dict_key))
                    if dict_key in file_to_compress:

                        # 保证输出文件夹存在
                        out_dir = os.path.join(output_dir, d)
                        out_file = os.path.join(out_dir, ssf)
                        # 保证指定drawable文件夹存在
                        if not os.path.exists(out_dir):
                            os.makedirs(out_dir)
                        if os.path.exists(file_path) and not os.path.exists(out_file):
                            shutil.copy(file_path, out_file)

    # 压缩文件夹下地图片
    if len(file_to_compress) > 0:
        out = tool.compress(output_dir)
        print("shirnked:" + str(out))
    # 复制压缩的文件回原来的路径
    copyTree(output_dir, res_floder)  # 删除临时输出文件夹
    if output_dir:
        shutil.rmtree(output_dir)
    if temp_dict:
        os.remove(temp_dict)
    # 更新图片的dict
    MakeResPicDict.make_res_pic_dict(res_floder, old_dict_file)


def usage():
    print '------------apkcompare.py usage:------------'
    print '-h, --help     : print help message.'
    print '-r, --res      : input weibo res floder path'
    print '-t, --tool     : ImageOptim path.'
    print '-d, --dict     : ResPicDict file path.'
    print '-o, --out      : Temp out dir.'
    print '----------------------------------------'


def exit():
    usage()
    sys.exit(1)


if "__main__" == __name__:
    res_floder = None
    tool = None
    old_dict = None
    out_floder = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:t:d:o:", ["help", "output="])

        # check all param
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage();
                sys.exit(1);
            if opt in ("-r", "--res"):
                res_floder = arg
            if opt in ("-t", "--tool"):
                tool = arg
            if opt in ("-d", "--dict"):
                old_dict = arg
            if opt in ("-o", "--out"):
                out_floder = arg

    except getopt.GetoptError, e:
        print("getopt error! " + e.msg);
        exit()

    if res_floder is None or tool is None or old_dict is None:
        exit()
        # TODO mail
    compress_diff_file(res_floder, tool + '/Contents/MacOS/ImageOptim', old_dict, out_floder)
