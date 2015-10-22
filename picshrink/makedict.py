#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

RES_FLODER = ".../res"
COMPARE_DICT = ".../res_pic_dict.txt"
WHITE_LIST_FILE = ".../res_compress_white_list"

command = "python MakeResPicDict.py -r %s -o %s -w %s" % (
    RES_FLODER, COMPARE_DICT, WHITE_LIST_FILE)
os.popen(command).read()
