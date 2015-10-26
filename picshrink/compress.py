#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

RES_FLODER = ".../res"
IMAGE_OPTIM_PATH = ".../ImageOptim.app"
COMPARE_DICT = ".../build-tools/res_pic_dict"
WHITE_LIST_FILE = ".../build-tools/res_compress_white_list"
OUT_TEMP_FLODER = ".../weibo_dev_res_git/bin"

command = "python CompressChangedPic.py -r %s -t %s -d %s -o %s -w %s" % (
    RES_FLODER, IMAGE_OPTIM_PATH, COMPARE_DICT, OUT_TEMP_FLODER, WHITE_LIST_FILE)

try:
    out = os.popen(command).read()
except Exception, e:
    out = e.message

print(out)