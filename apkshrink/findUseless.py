#! /usr/bin/env python
# -*- coding: utf-8 -*-
from lib_apk_shrink.instrument.UselessDrawable import UselessDrawable

__author__ = 'tiantong'
import os
import sys

from lib_apk_shrink.instrument.JarDecompile import JarDecompile
from lib_apk_shrink.instrument.UselessLayout import UselessLayout
from apkshrink import shrink_loader

sys.path.append("")

USELESS_LAYOUT_FILE = ''
DECOMPILE_FILE = ''
USELESS_DRAWABLE_FILE = ''

# 清空旧的文本内容
file_to_delete = ["UselessLayout.txt", "UselessDrawable.txt"]
for file in file_to_delete:
    if os.path.isfile(file):
        f = open(file, 'w')
        f.close()

uselessLayoutConfig = shrink_loader.init_useless_layout_config(USELESS_LAYOUT_FILE)
decompileConfig = shrink_loader.init_decompile_config(DECOMPILE_FILE)
uselessDrawableConfig = shrink_loader.init_useless_drawbale_config(USELESS_DRAWABLE_FILE)

# 反编译 extra jar
jarDecompile = JarDecompile(decompileConfig)
jarDecompile.decompile_jar()

# 查找无用的layout
uselessLayout = UselessLayout(uselessLayoutConfig)
uselessLayout.extra_jar_path = jarDecompile.output_path_decompile
uselessLayout.fast_search = True
uselessLayout.check_useless_layout()
uselessLayout.writeResult()

# drawable
uselessDrawbale = UselessDrawable(uselessDrawableConfig)
uselessDrawbale.extra_jar_path = jarDecompile.output_path_decompile
uselessDrawbale.fast_search = True
uselessDrawbale.check_useless_drawable()
uselessDrawbale.writeResult()

# TODO 查找无用的drawable 

# 清楚反编译时候临时输出的文件
jarDecompile.clearOutput()
