#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class UselessLayoutConfig(object):
    src_dir = []
    layout_dir = []
    xml_dir = []
    white_list = []

    def __init__(self, dict=[]):
        if 'src_dir' in dict:
            self.src_dir = dict['src_dir']
        if 'layout_dir' in dict:
            self.layout_dir = dict['layout_dir']
        if 'xml_dir' in dict:
            self.xml_dir = dict['xml_dir']
        if 'white_list' in dict:
            self.white_list = dict['white_list']

    def __repr__(self):
        return 'UselessLayoutConfig'
