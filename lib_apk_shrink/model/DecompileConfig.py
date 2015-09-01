#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class DecompileConfig(object):
    jad_path = ""
    output_path = ""
    extra_jar = []

    def __init__(self, dict=[]):
        if 'jad_path' in dict:
            self.jad_path = dict['jad_path']
        if 'output_path' in dict:
            self.output_path = dict['output_path']
        if 'extra_jar' in dict:
            self.extra_jar = dict['extra_jar']

    def __repr__(self):
        return 'DecompileConfig'
