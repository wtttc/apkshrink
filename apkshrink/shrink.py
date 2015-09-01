#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tiantong'
import sys

sys.path.append("")

import datetime
import os

from lib_apk_shrink.compress.ImageOptim import ImageOptim
from lib_apk_shrink.instrument.AlphaCheck import AlphaCheck
from lib_apk_shrink.instrument.PngCompress import PngCompress
from lib_apk_shrink.instrument.SizeCheck import SizeCheck
from apkshrink import mail_util, shrink_loader

COMPRESS_STATE_FILE = ''
COMPRESS_CONFIG_FILE = ''
CHECK_SIZE_CONFIG_FILE = ''
CHECK_ALPHA_CONFIG_FILE = ''
WEBP_CONFIG_FILE = ''


# 清空旧的文本内容
file_to_delete = ["AlphaCheck.txt", "PngCompress.txt", "SizeCheck.txt"]
for file in file_to_delete:
    if os.path.isfile(file):
        f = open(file, 'w')
        f.close()

# 获取初始化参数
compressConfig = shrink_loader.init_compress_config(COMPRESS_CONFIG_FILE)
compressState = shrink_loader.init_compress_state(COMPRESS_STATE_FILE)
tool = ImageOptim("")

# 压缩图片
pngCompress = PngCompress(compressConfig, compressState.last_update_time, tool)
pngCompress.compress_all_png()

# 保存状态
last_time = compressState.last_update_time;
compressState.last_update_time = datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S');
compressState.last_compressed_count = pngCompress.compressed_count
compressState.last_compressed_size = pngCompress.compressed_size
compressState.total_compressed_count += pngCompress.compressed_count
compressState.total_compressed_size += pngCompress.compressed_size
shrink_loader.write_compress_state(COMPRESS_STATE_FILE, compressState)

root_floder = "res"
# 检查图片透明度
alphaConfig = shrink_loader.init_check_alpha_config(CHECK_ALPHA_CONFIG_FILE)
alphaCheck = AlphaCheck(alphaConfig)
alphaCheck.check_png_with_alpha(root_floder)

# 检查太大的图片
sizeConfig = shrink_loader.init_check_size_config(CHECK_SIZE_CONFIG_FILE)
sizeCheck = SizeCheck(sizeConfig)
sizeCheck.check_png_size_scale(root_floder)

# TODO 检查无用资源

# 将结果发送邮件
# EMAIL_FROM = ""
# EMAIL_TO = [""]
# USER_NAME = ""
# PASSWORD = ""
# mail_util.sendMail("lalalal", EMAIL_FROM, EMAIL_TO, USER_NAME, PASSWORD, file_to_delete)
