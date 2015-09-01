#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tiantong'
import datetime
import os

from lib_apk_shrink.model.CompressConfig import CompressConfig
from lib_apk_shrink.utils import shrink_utils
from lib_apk_shrink.log.Logger import Logger

log = Logger(logname='PngCompress.txt', loglevel=0, logger="PngCompress").getlog()


class PngCompress(object):
    # 压缩图片的配置
    compress_config = CompressConfig()
    # 上次最后的更新时间
    last_update_time = 0

    # 本次压缩的个数
    compressed_count = 0
    # 本次压缩总共的大小
    compressed_size = 0

    tool = None;

    def __init__(self, compressConfig, lastUpdateTime, tool):
        self.compress_config = compressConfig
        self.last_update_time = lastUpdateTime
        self.tool = tool

    def compress_png(self, parent, filename):
        # 获取文件的绝对路径
        path = os.path.join(parent, filename)

        # 过滤文件夹
        if os.path.isdir(path):
            return None

        # 过滤文件类型
        if not os.path.splitext(filename)[1] in self.compress_config.compress_format:
            return None

        # 略过上次压缩到现在都没有修改过的文件
        t = os.path.getmtime(path)
        # 修改unix时间戳为time对象
        timestamp = datetime.datetime.fromtimestamp(t)
        if timestamp <= self.last_update_time:
            log.info(filename + ": HAS NOT UPDATE SINCE LAST_UPDATE_TIME")
            log.info("")
            return None

        # 过滤关键字
        skip = False
        for ignore in self.compress_config.compress_ignore_pattern:
            if ignore in filename:
                log.info("IGNORE:" + ignore + " in " + filename + " NO NEED TO COMPRESS")
                log.info("")
                skip = True
        if skip:
            return None

        # 执行压缩命令
        if filename:
            log.info("IMAGE:" + filename)
            result = None
            try:
                if ".9." in filename:
                    # result = patch_tool.compress(path)
                    pass
                else:
                    if self.tool is not None:
                        result = self.tool.compress(path)
            except Exception, e:
                print e
                return None

            if result is not None:
                # 压缩计数器+1
                self.compressed_count += 1
                # 压缩值累加
                self.compressed_size += int(result)
                log.info("CHANGED: " + str(result) + "(byte)")
            else:
                log.info("NO COMPRESSION")

            log.info("")

    # 遍历要扫描的文件夹
    @shrink_utils.performance()
    def compress_all_png(self):
        for BASE_DIR in self.compress_config.compress_dir:
            # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for parent, dirnames, filenames in os.walk(BASE_DIR):
                for filename in filenames:
                    if self.compress_png(parent, filename) is None:
                        continue
