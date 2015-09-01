#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tiantong'
import os

from lib_apk_shrink.model.CheckSizeConfig import CheckSizeConfig
from lib_apk_shrink.utils import shrink_utils
from lib_apk_shrink.log.Logger import Logger

log = Logger(logname='SizeCheck.txt', loglevel=0, logger="SizeCheck", hasformat=False).getlog()


class SizeCheck(object):
    size_config = CheckSizeConfig()
    file_list = []
    total_ignore_size = 0
    total_too_big_size = 0

    def __init__(self, sizeConfig=CheckSizeConfig()):
        self.size_config = sizeConfig

    def check_png_size_scale(self, floder_root):
        # 遍历要扫描的文件夹s
        for BASE_DIR in self.size_config.check_size_dir:
            # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for parent, dir_names, filenames in os.walk(BASE_DIR):
                # 遍历所有文件
                for filename in filenames:

                    path = os.path.join(parent, filename)
                    size = os.path.getsize(path)
                    size_scale = self.size_config.size_scale_normal

                    if filename in self.size_config.check_size_ignore_list:
                        self.total_ignore_size += size
                        continue

                    # 过滤设置fileType1的sizeScale
                    if os.path.splitext(filename)[1] in self.size_config.file_type_1:
                        size_scale = self.size_config.size_scale_1

                    if size >= size_scale:
                        self.total_too_big_size += size
                        log.info("file:" + shrink_utils.get_folder_name(parent, floder_root) + os.sep + filename)
                        log.info("size:" + shrink_utils.convert_bytes(size))
                        log.info("")
