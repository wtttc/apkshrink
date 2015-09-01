#! /usr/bin/env python
# -*- coding: utf-8 -*-
#


class CheckSizeConfig(object):
    check_size_dir = []
    check_size_ignore_list = []
    size_scale_normal = 100000
    size_scale_1 = 100000
    file_type_1 = ""

    def __init__(self, dict=[]):
        # 检查目录的绝对路径
        if 'check_size_dir' in dict:
            self.check_size_dir = dict['check_size_dir']
        # ignore的对象
        if 'check_size_ignore_list' in dict:
            self.check_size_ignore_list = dict['check_size_ignore_list']
        # 普通文件大小的限制 50k
        if 'size_scale_normal' in dict:
            self.size_scale_normal = dict['size_scale_normal']
        # 针对特殊文件大小的限制，可拓展添加
        # zip文件 -> 100k
        if 'sizeScale1' in dict:
            self.size_scale_1 = dict['sizeScale1']
        if 'fileType1' in dict:
            self.file_type_1 = dict['fileType1']

    def __repr__(self):
        return 'CheckSizeConfig'
