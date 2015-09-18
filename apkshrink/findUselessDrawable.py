#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

__author__ = 'tiantong'
rootdir = "/Users/easytang/Documents/Git/github/apkshrink"
sys.path.append(rootdir)

from apkshrink import shrink_loader
from lib_apk_shrink.instrument.UselessDrawable import UselessDrawable
from lib_apk_shrink.instrument.JarDecompile import JarDecompile

USELESS_DRAWABLE_FILE = rootdir + '/config/res_useless_drawable_config.json'
DECOMPILE_FILE = rootdir + '/config/res_decompile_config.json'

# 清空旧的文本内容
file_to_delete = ["UselessDrawable.txt"]
for file in file_to_delete:
    if os.path.isfile(file):
        f = open(file, 'w')
        f.close()

decompileConfig = shrink_loader.init_decompile_config(DECOMPILE_FILE)
uselessDrawableConfig = shrink_loader.init_useless_drawbale_config(USELESS_DRAWABLE_FILE)

# 反编译 extra jar
jarDecompile = JarDecompile(decompileConfig)
jarDecompile.decompile_jar()

# drawable
uselessDrawbale = UselessDrawable(uselessDrawableConfig)
uselessDrawbale.extra_jar_path = jarDecompile.output_path_decompile
uselessDrawbale.fast_search = True
uselessDrawbale.check_useless_drawable()
uselessDrawbale.writeResult()
uselessDrawbale.deleteUseless()


# 清楚反编译时候临时输出的文件
jarDecompile.clearOutput()
