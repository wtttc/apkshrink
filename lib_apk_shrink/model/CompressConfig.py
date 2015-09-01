#! /usr/bin/env python
# -*- coding: utf-8 -*-


class CompressConfig(object):
    compress_dir = []
    compress_format = []
    compress_ignore_pattern = []

    def __init__(self, dict=[]):
        # 压缩扫描文件夹的绝对路径
        if 'compress_dir' in dict:
            self.compress_dir = dict['compress_dir']
        # 压缩对象的格式
        if 'compress_format' in dict:
            self.compress_format = dict['compress_format']
        # 压缩忽略的patterner(当前只有.9)
        if 'compress_ignore_pattern' in dict:
            self.compress_ignore_pattern = dict['compress_ignore_pattern']

    def __repr__(self):
        return 'CompressConfig'
