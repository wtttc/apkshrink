#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

__author__ = 'tiantong'
rootdir = "/Users/easytang/Documents/Git/github/apkshrink"
sys.path.append(rootdir)

from apkshrink import shrink_loader
from lib_apk_shrink.instrument.AlphaCheck import AlphaCheck

CHECK_ALPHA_CONFIG_FILE = rootdir + '/config/res_check_alpha_config.json'


# 清空旧的文本内容
file_to_delete = ["AlphaCheck.txt"]
for file in file_to_delete:
    if os.path.isfile(file):
        f = open(file, 'w')
        f.close()

root_floder = "res"
# 检查图片透明度
alphaConfig = shrink_loader.init_check_alpha_config(CHECK_ALPHA_CONFIG_FILE)
alphaCheck = AlphaCheck(alphaConfig)
alphaCheck.check_png_with_alpha(root_floder)
