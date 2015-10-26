#! /usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import os
import sys
import shutil

import MakeResPicDict
import Utils

__author__ = 'tiantong'

RES_NAME = "res" + os.path.sep

# BatchShrink [file path]
class BatchShrink(object):
    def __init__(self, command):
        self.command = command

    def compress(self, floder_string):
        command = self.command + " " + floder_string

        old_size = Utils.get_path_size(floder_string);
        out = ""
        try:
            cmd_out = os.popen(command).read()
            out += cmd_out
        except Exception, e:
            out += e.message

        if len(out) > 0:
            print("")
            print("ImageOptim output:" + out)
            print("")
        new_size = Utils.get_path_size(floder_string);
        chg_size = long(old_size) - long(new_size)
        return chg_size;


def compress_diff_file(res_floder, tool, old_dict_file, out_floder=None, white_list_file=None):
    # 初始化工具和参数
    tool = BatchShrink(tool)
    # 获取原始dict
    old_dict = Utils.read_dict_from_file(old_dict_file)
    # 获取白名单
    white_list_set = None
    if white_list_file is not None:
        white_list_set = Utils.read_set_from_file(white_list_file)
    # 获取临时输出文件
    if out_floder is None:
        out_floder = os.path.join(Utils.cur_file_dir(), "temp")
    else:
        out_floder = os.path.join(out_floder, "temp")

    # 保证temp存在
    if not os.path.exists(out_floder):
        os.makedirs(out_floder)

    # 临时dict位置
    temp_dict = out_floder + os.path.sep + "temp_dict"
    # print("temp file path:" + str(temp_dict))

    success = 0

    try:
        # 生成临时dict，用作比对
        MakeResPicDict.make_res_pic_dict(res_floder, temp_dict, white_list_file)
        new_dict = Utils.read_dict_from_file(temp_dict)

        # 对比检查出新修改的文件
        file_to_compress = set()

        # 检查出新增和变化的图片文件
        for k, v in new_dict.items():
            if old_dict is not None and k in old_dict:
                if old_dict[k] != new_dict[k]:
                    # changed
                    file_to_compress.add(k)
            else:
                # new
                file_to_compress.add(k)

        if len(file_to_compress) > 0:
            print("file_to_compress:")
            for item in file_to_compress:
                print("file: " + str(item))
        else:
            print("There's no file to compress")


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
                            if white_list_set is not None and ssf in white_list_set:
                                print("file:" + ssf + " is filtered")
                                continue
                            # 保证输出文件夹存在
                            out_dir = os.path.join(out_floder, d)
                            out_file = os.path.join(out_dir, ssf)
                            # 保证指定drawable文件夹存在
                            if not os.path.exists(out_dir):
                                os.makedirs(out_dir)
                            if os.path.exists(file_path) and not os.path.exists(out_file):
                                shutil.copy(file_path, out_file)

        # 压缩文件夹下地图片
        print("")
        if len(file_to_compress) > 0:
            out = tool.compress(out_floder)
            print("shirnked " + str(len(file_to_compress)) + " files")
            print("shirnked:" + Utils.get_size_in_nice_string(out))
    except Exception, e:
        success = 1

    # 移除临时dict
    if os.path.isfile(temp_dict):
        os.remove(temp_dict)
    # 复制压缩的文件回原来的路径
    if success == 0:
        Utils.copyTree(out_floder, res_floder)
    # 删除临时输出文件夹
    if out_floder:
        shutil.rmtree(out_floder)
    # 更新图片的dict
    MakeResPicDict.make_res_pic_dict(res_floder, old_dict_file, white_list_file)


def usage():
    print '------------apkcompare.py usage:------------'
    print '-h, --help      : print help message.'
    print '-r, --res       : input weibo res floder path'
    print '-t, --tool      : ImageOptim path.'
    print '-d, --dict      : ResPicDict file path.'
    print '-o, --out       : Temp out dir.'
    print '-w, --whitelist : White list.'
    print '----------------------------------------'


def exit():
    usage()
    sys.exit(1)


if "__main__" == __name__:
    res_floder = None
    tool = None
    old_dict = None
    out_floder = None
    white_list_file = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:t:d:o:w:", ["help", "output="])

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
            if opt in ("-w", "--whitelist"):
                white_list_file = arg

    except getopt.GetoptError, e:
        print("getopt error! " + e.msg);
        exit()

    if res_floder is None or tool is None or old_dict is None:
        exit()

    compress_diff_file(res_floder, tool + '/Contents/MacOS/ImageOptim', old_dict, out_floder, white_list_file)
