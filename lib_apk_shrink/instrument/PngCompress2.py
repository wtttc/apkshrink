#! /usr/bin/env python
# -*- coding: utf-8 -*-
import shutil

__author__ = 'tiantong'
import datetime
import os

from lib_apk_shrink.model.CompressConfig import CompressConfig
from lib_apk_shrink.utils import shrink_utils
from lib_apk_shrink.log.Logger import Logger

log = Logger(logname='PngCompress2.txt', loglevel=0, logger="PngCompress2").getlog()


class PngCompress2(object):
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

    def compress_dir(self, dir):
        self.compressed_size = self.tool.compress(dir)

    # 遍历要扫描的文件夹
    @shrink_utils.performance()
    def compress_all_png(self):
        for BASE_DIR in self.compress_config.compress_dir:
            output_dir = os.path.join(BASE_DIR, "temp")
            # 保证temp存在
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            for parent, dirnames, filenames in os.walk(BASE_DIR):
                for dirname in dirnames:
                    # 过滤掉非drawable的目录
                    if "drawable" in dirname:
                        folder_path = os.path.join(parent, dirname)
                        log.info("")
                        log.info(folder_path)
                        for s_parent, s_dirnames, s_filenames in os.walk(folder_path):
                            self.walk_pic_valid(s_parent, dirname, s_filenames, output_dir)
            # 压缩文件夹下地图片
            self.compress_dir(output_dir);
            # 复制压缩的文件回原来的路径
            shrink_utils.copyTree(output_dir, BASE_DIR)
            # 删除临时输出文件夹
            if output_dir:
                shutil.rmtree(output_dir)

    def walk_pic_valid(self, parent, dirname, filenames, output_dir):
        for filename in filenames:

            path = os.path.join(parent, filename)
            log.info("path:" + path)

            # 过滤文件类型
            if not os.path.splitext(filename)[1] in self.compress_config.compress_format:
                continue

            # 略过上次压缩到现在都没有修改过的文件
            t = os.path.getmtime(path)
            # 修改unix时间戳为time对象
            timestamp = datetime.datetime.fromtimestamp(t)
            if timestamp <= self.last_update_time:
                log.info(filename + ": HAS NOT UPDATE SINCE LAST_UPDATE_TIME")
                log.info("")
                continue

            # 过滤关键字
            skip = False
            for ignore in self.compress_config.compress_ignore_pattern:
                if ignore in filename:
                    log.info("IGNORE:" + ignore + " in " + filename + " NO NEED TO COMPRESS")
                    log.info("")
                    skip = True
            if skip:
                continue

            # 确认输入输出路径
            in_string = os.path.join(parent, filename)
            log.info("in_string:" + in_string)
            out_string = os.path.join(output_dir, dirname, filename)
            log.info("out_string:" + out_string)

            # 保证输出文件夹存在
            cur_dir = os.path.join(output_dir, dirname)
            # 保证res存在
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # 保证指定drawable文件夹存在
            if not os.path.exists(cur_dir):
                os.makedirs(cur_dir)

            if ".9." in filename:
                pass
            else:
                log.info("find normal in " + dirname + " file " + filename)
                if os.path.exists(in_string) and not os.path.exists(out_string):
                    shutil.copy(in_string, out_string)
                    self.compressed_count += 1
