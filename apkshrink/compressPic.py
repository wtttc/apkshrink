#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import os

__author__ = 'tiantong'
rootdir = "/Users/easytang/Documents/Git/github/apkshrink"
sys.path.append(rootdir)

from lib_apk_shrink.compress.BatchShrink import BatchShrink
from lib_apk_shrink.instrument.PngCompress2 import PngCompress2
from apkshrink import shrink_loader

COMPRESS_STATE_FILE = rootdir + '/config/res_compress_state.json'
COMPRESS_CONFIG_FILE = rootdir + '/config/res_compress_config.json'
TOOL_PATH = rootdir + "/libs/ImageOptim.app/Contents/MacOS/ImageOptim"


# 清空旧的文本内容
file_to_delete = ["PngCompress.txt"]
for file in file_to_delete:
    if os.path.isfile(file):
        f = open(file, 'w')
        f.close()

# 获取初始化参数
compressConfig = shrink_loader.init_compress_config(COMPRESS_CONFIG_FILE)
compressState = shrink_loader.init_compress_state(COMPRESS_STATE_FILE)
tool = BatchShrink(TOOL_PATH)

# 压缩图片
pngCompress = PngCompress2(compressConfig, compressState.last_update_time, tool)
pngCompress.compress_all_png()

# 保存状态
last_time = compressState.last_update_time;
compressState.last_update_time = datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S');
compressState.last_compressed_count = pngCompress.compressed_count
compressState.last_compressed_size = pngCompress.compressed_size
compressState.total_compressed_count += pngCompress.compressed_count
compressState.total_compressed_size += pngCompress.compressed_size
shrink_loader.write_compress_state(COMPRESS_STATE_FILE, compressState)

# 将结果发送邮件
# EMAIL_FROM = ""
# EMAIL_TO = [""]
# USER_NAME = ""
# PASSWORD = ""
# mail_util.sendMail("lalalal", EMAIL_FROM, EMAIL_TO, USER_NAME, PASSWORD, file_to_delete)
