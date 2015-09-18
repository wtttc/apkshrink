#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

__author__ = 'tiantong'
rootdir = "/Users/easytang/Documents/Git/github/apkshrink"
sys.path.append(rootdir)

from apkshrink import shrink_loader
from lib_apk_shrink.instrument.SizeCheck import SizeCheck

CHECK_SIZE_CONFIG_FILE = rootdir + '/config/res_check_size_config.json'

# 清空旧的文本内容
file_to_delete = ["SizeCheck.txt"]
for file in file_to_delete:
    if os.path.isfile(file):
        f = open(file, 'w')
        f.close()

root_floder = "res"
# 检查太大的图片
sizeConfig = shrink_loader.init_check_size_config(CHECK_SIZE_CONFIG_FILE)
sizeCheck = SizeCheck(sizeConfig)
sizeCheck.check_png_size_scale(root_floder)
