#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tiantong'
import os

import numpy
from PIL import Image

from lib_apk_shrink.model.CheckAlphaConfig import CheckAlphaConfig
from lib_apk_shrink.utils import shrink_utils
from lib_apk_shrink.log.Logger import Logger

log = Logger(logname='AlphaCheck.txt', loglevel=0, logger="AlphaCheck", hasformat=False).getlog()


class AlphaCheck(object):
    alpah_config = CheckAlphaConfig()
    file_list = []

    def __init__(self, alphaConfig=CheckAlphaConfig()):
        self.alpah_config = alphaConfig

    def check_png_with_alpha(self, floder_root):
        count = 0
        # 遍历要扫描的文件夹s
        for BASE_DIR in self.alpah_config.check_alpha_dir:
            # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for parent, dir_names, filenames in os.walk(BASE_DIR):
                for filename in filenames:
                    # 获取文件的绝对路径
                    path = os.path.join(parent, filename)

                    # 过滤文件类型
                    if not os.path.splitext(filename)[1] in self.alpah_config.check_alpha_format:
                        continue

                    # 判断文件存在
                    if not filename:
                        continue

                    # 检查文件类型
                    mode = self.check_img_mode(path)
                    # print filename + ": " + mode
                    if mode != 'RGB':
                        continue

                    # 检查文件阈值范围
                    size = os.path.getsize(path)
                    # print "size: " + str(size)
                    if size < self.alpah_config.size_scale:
                        continue

                    log.info('IMAGE:' + shrink_utils.get_folder_name(parent, floder_root) + os.sep + filename)
                    count += 1

        if count > 0:
            log.info('These ' + str(
                count) + ' image(s) may be pngs with no alpha and size larger than %s, considering jpeg?' % (
                         shrink_utils.get_size_in_nice_string(self.alpah_config.size_scale)))
        log.info("")

    @classmethod
    def check_img_mode(cls, filedir):
        try:
            img = Image.open(filedir)
        except Exception, ex:
            err_info = 'This is not image: ' + str(filedir) + '\n'
            print err_info
            return err_info
        try:
            if img.mode == "RGBA":
                alpha = img.split()[3]
                arr = numpy.asarray(alpha)
                count = 0
                for i in range(0, img.size[0] - 1):
                    for j in range(0, img.size[1] - 1):
                        if arr[j][i] < 128:
                            count += 1
                            break;
                if count == 0:
                    return "RGB"
        except Exception, ex:
            pass
        return img.mode
