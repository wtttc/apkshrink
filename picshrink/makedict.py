#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

RES_FLODER = ".../res"
COMPARE_DICT = ".../build-tools/res_pic_dict"
WHITE_LIST_FILE = ".../build-tools/res_compress_white_list"

command = "python MakeResPicDict.py -r %s -o %s -w %s" % (
    RES_FLODER, COMPARE_DICT, WHITE_LIST_FILE)

try:
    out = os.popen(command).read()
except Exception, e:
    out = e.message

print(out)
