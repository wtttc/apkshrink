#! /usr/bin/env python
# -*- coding: utf-8 -*-


class WebPConfig(object):
    command = ""
    command_opt = ""
    compress_dir = []
    out_suffix = ""
    compress_ignore_pattern = []

    def __init__(self, dict=[]):
        # 执行的绝对路径命令
        if 'command' in dict:
            self.command = dict['command']
        # webP的配置
        if 'command_opt' in dict:
            self.command_opt = dict['command_opt']
            # 压缩扫描文件夹的绝对路径
        if 'compress_dir' in dict:
            self.compress_dir = dict['compress_dir']
        # 输出文件后缀
        if 'out_suffix' in dict:
            self.out_suffix = dict['out_suffix']
        # 压缩忽略的patterner(当前只有.9)
        if 'compress_ignore_pattern' in dict:
            self.compress_ignore_pattern = dict['compress_ignore_pattern']

    def __repr__(self):
        return 'WebPConfig'
