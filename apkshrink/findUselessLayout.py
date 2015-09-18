#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

__author__ = 'tiantong'
rootdir = "/Users/easytang/Documents/Git/github/apkshrink"
sys.path.append(rootdir)

from apkshrink import shrink_loader
from lib_apk_shrink.instrument.JarDecompile import JarDecompile
from lib_apk_shrink.instrument.UselessLayout import UselessLayout

USELESS_LAYOUT_FILE = rootdir + '/config/res_useless_layout_config.json'
DECOMPILE_FILE = rootdir + '/config/res_decompile_config.json'

# 清空旧的文本内容
file_to_delete = ["UselessLayout.txt"]
for file in file_to_delete:
    if os.path.isfile(file):
        f = open(file, 'w')
        f.close()

uselessLayoutConfig = shrink_loader.init_useless_layout_config(USELESS_LAYOUT_FILE)
decompileConfig = shrink_loader.init_decompile_config(DECOMPILE_FILE)

# 反编译 extra jar
jarDecompile = JarDecompile(decompileConfig)
jarDecompile.decompile_jar()

# 查找无用的layout
uselessLayout = UselessLayout(uselessLayoutConfig)
uselessLayout.extra_jar_path = jarDecompile.output_path_decompile
uselessLayout.fast_search = True
uselessLayout.check_useless_layout()
uselessLayout.writeResult()
uselessLayout.deleteUseless()

# 清楚反编译时候临时输出的文件
jarDecompile.clearOutput()
