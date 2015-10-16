#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class UselessDrawableConfig(object):
    src_dir = []
    res_dir = []
    extra = []
    white_list = []

    def __init__(self, dict=[]):
        if 'src_dir' in dict:
            self.src_dir = dict['src_dir']
        if 'res_dir' in dict:
            self.res_dir = dict['res_dir']
        if 'extra' in dict:
            self.extra = dict['extra']
        if 'white_list' in dict:
            self.white_list = dict['white_list']

    def __repr__(self):
        return 'UselessDrawableConfig'
