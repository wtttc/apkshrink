#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import sys
from lib_apk_shrink.utils import shrink_utils

reload(sys)
sys.setdefaultencoding("utf-8")

SUCCESS = 1
CONTINUE = 2


def convert_to_webp(parent, filename):
    # 获取文件的绝对路径
    path = os.path.join(parent, filename)

    # 过滤文件夹
    if os.path.isdir(path):
        return CONTINUE

    # 过滤关键字
    skip = False
    for ignore in WEBP_IGNORE_PATTERN:
        if ignore in filename:
            print "IGNORE:" + ignore + " in " + filename + " NO NEED TO COMPRESS"
            skip = True
    if skip:
        return CONTINUE

    # 执行压缩命令
    if filename:
        try:
            print 'IMAGE:', filename
            portion = os.path.splitext(path)
            new_name = portion[0] + WEBP_OUT_SURFFIX
            new_path = os.path.join(parent, new_name)
            command = WEBP_COMMAND + WEBP_COMMAND_OPT + path + " -o " + new_path
            result = os.popen(command).read()
            print result
            os.remove(path)
        except Exception, e:
            print e
            return CONTINUE


# 遍历要扫描的文件夹
@shrink_utils.performance()
def convert_all_png_to_webp(dirs):
    for BASE_DIR in dirs:
        # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for parent, dir_names, filenames in os.walk(BASE_DIR):
            for filename in filenames:
                if convert_to_webp(parent, filename) == CONTINUE:
                    continue

# 从配置文件中读取设置
webp_config = shrink_utils.init_webp_config();
if not webp_config:
    print "LOAD webPConfig FAILED"
    exit()
WEBP_COMMAND = webp_config.command
WEBP_COMMAND_OPT = webp_config.command_opt
WEBP_COMPRESS_DIR = webp_config.compress_dir
WEBP_OUT_SURFFIX = webp_config.out_suffix
WEBP_IGNORE_PATTERN = webp_config.compress_ignore_pattern
print "WEBP_COMMAND:", WEBP_COMMAND
print "WEBP_COMMAND_OPT:", WEBP_COMMAND_OPT
print "WEBP_COMPRESS_DIR:", WEBP_COMPRESS_DIR
print "WEBP_OUT_SURFFIX:", WEBP_OUT_SURFFIX
print "WEBP_IGNORE_PATTERN:", WEBP_IGNORE_PATTERN

convert_all_png_to_webp(WEBP_COMPRESS_DIR)
