#! /usr/bin/env python
# -*- coding: utf-8 -*-
#


class CheckAlphaConfig(object):
    check_alpha_dir = []
    check_alpha_ignore_list = []
    check_alpha_format = []
    size_scale = 1000000

    def __init__(self, dict=[]):
        # 检查目录的绝对路径
        if 'check_alpha_dir' in dict:
            self.check_alpha_dir = dict['check_alpha_dir']
        # ignore的对象
        if 'check_alpha_ignore_list' in dict:
            self.check_alpha_ignore_list = dict['check_alpha_ignore_list']
        # 检查的文件类型
        if 'check_alpha_format' in dict:
            self.check_alpha_format = dict['check_alpha_format']
        # 文件大小的阈值
        if 'size_scale' in dict:
            self.size_scale = dict['size_scale']

    def __repr__(self):
        return 'CheckAlphaConfig'
