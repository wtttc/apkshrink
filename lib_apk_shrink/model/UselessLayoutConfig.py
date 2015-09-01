#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class UselessLayoutConfig(object):
    src_dir = []
    layout_dir = []

    def __init__(self, dict=[]):
        if 'src_dir' in dict:
            self.src_dir = dict['src_dir']
        if 'layout_dir' in dict:
            self.layout_dir = dict['layout_dir']

    def __repr__(self):
        return 'UselessLayoutConfig'
