#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class UselessDrawableConfig(object):
    src_dir = []
    res_dir = []
    extra_xml = []

    def __init__(self, dict=[]):
        if 'src_dir' in dict:
            self.src_dir = dict['src_dir']
        if 'res_dir' in dict:
            self.res_dir = dict['res_dir']
        if 'extra_xml' in dict:
            self.extra_xml = dict['extra_xml']

    def __repr__(self):
        return 'UselessDrawableConfig'
