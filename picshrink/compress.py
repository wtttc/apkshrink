#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

RES_FLODER = ".../res"
IMAGE_OPTIM_PATH = ".../ImageOptim.app"
COMPARE_DICT = ".../res_pic_dict.txt"
WHITE_LIST_FILE = ".../res_compress_white_list"
OUT_TEMP_FLODER = ".../bin"

command = "python CompressChangedPic.py -r %s -t %s -d %s -o %s -w %s" % (
    RES_FLODER, IMAGE_OPTIM_PATH, COMPARE_DICT, OUT_TEMP_FLODER, WHITE_LIST_FILE)
os.popen(command).read()
