#! /usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'tiantong'


class BaseCompressTool(object):
    command = ""

    def __init__(self, command):
        self.command = ""

    # 执行压缩，返回变化的size
    def compress(self, file_string):
        pass
