#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import datetime


class CompressState(object):
    last_update_time = ''
    last_compressed_count = 0
    last_compressed_size = 0
    total_compressed_count = 0
    total_compressed_size = 0

    def __init__(self, dict=[]):
        if 'last_update_time' in dict:
            self.last_update_time = datetime.datetime.strptime(dict['last_update_time'], '%m-%d-%y %H:%M:%S')
        if 'last_compressed_count' in dict:
            self.last_compressed_count = dict['last_compressed_count']
        if 'last_compressed_size' in dict:
            self.last_compressed_size = dict['last_compressed_size']
        if 'total_compressed_count' in dict:
            self.total_compressed_count = dict['total_compressed_count']
        if 'total_compressed_size' in dict:
            self.total_compressed_size = dict['total_compressed_size']

    def __repr__(self):
        return 'CompressState'
