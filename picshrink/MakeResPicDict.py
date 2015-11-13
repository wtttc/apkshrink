#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tiantong'

import hashlib
import os
import getopt
import sys

import Utils

FILE_TYPE = ["png", "jpg", "jpeg", "bmp"]
FILTER_LIST = [".9.", ".DS_Store"]
RES_NAME = os.path.sep + "res" + os.path.sep


# 过滤文件
def find_filter(filename):
    for item in FILTER_LIST:
        if item in str(filename):
            return True
    return False


# 过滤图片文件
def find_match(filename):
    for item in FILE_TYPE:
        if item in str(filename):
            return True
    return False


def calc_MD5(filepath):
    try:  # 以二进制的形式打开
        with open(filepath, 'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            return hash
    except Exception, ex:
        print "Error:" + str(ex)
        return None


def make_res_pic_dict(res_floder, out_file, white_list_file=None):
    print("")
    print("Try to make file dict")
    white_list_set = None
    if white_list_file is not None:
        white_list_set = Utils.read_set_from_file(white_list_file)
    res_pic_dict = dict()

    for p, d, _ in os.walk(res_floder):
        for sd in d:
            # 查出带drawable的文件夹
            if "drawable" in sd:
                # print("find drawable floder:" + str(sd))
                pass
            else:
                continue
            sub_floder_path = os.path.join(p, sd)
            for sp, sd, f in os.walk(sub_floder_path):
                for sf in f:
                    if find_filter(sf):
                        continue
                    if not find_match(sf):
                        continue
                        # 获取到res/的路径
                    file_path = os.path.join(sp, sf)
                    dict_key_index = file_path.find(RES_NAME)
                    dict_key = file_path[dict_key_index:]
                    if white_list_set is not None and sf in white_list_set:
                        print("file:" + dict_key + " is filtered")
                        continue
                    dict_value = calc_MD5(file_path)
                    # print("dict_key:" + str(dict_key))
                    # print("dict_value:" + str(dict_value))
                    res_pic_dict[dict_key] = dict_value
    Utils.save_dict_to_file(out_file, res_pic_dict)


def usage():
    print '------------apkcompare.py usage:------------'
    print '-h, --help     : print help message.'
    print '-r, --res      : input weibo res floder path'
    print '-o, --out      : output file path'
    print '-w, --whitelist : White list.'
    print '----------------------------------------'


def exit():
    usage()
    sys.exit(1)


if "__main__" == __name__:
    res_floder = None
    out_file = None
    white_list_file = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:o:w:", ["help", "output="])

        # check all param
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage();
                sys.exit(1);
            if opt in ("-r", "--res"):
                res_floder = arg
            if opt in ("-o", "--out"):
                out_file = arg
            if opt in ("-w", "--whitelist"):
                white_list_file = arg

    except getopt.GetoptError, e:
        print("getopt error! " + e.msg);
        exit()

    if res_floder is None:
        exit()
    if out_file is None:
        print("output file is not set, default res_pic_dict.txt will be used.")
        out_file = Utils.cur_file_dir() + os.path.sep + "res_pic_dict.txt"
    print("")
    # print("res_floder:" + str(res_floder))
    # print("white_list_file:" + str(white_list_file))
    make_res_pic_dict(res_floder, out_file, white_list_file)
