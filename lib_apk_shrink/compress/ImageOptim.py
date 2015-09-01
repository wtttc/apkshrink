#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tiantong'
import os

from lib_apk_shrink.compress.BaseCompressTool import BaseCompressTool



# ImageOptim [file path]
# mac 版本没有命令行输出，不方便统计
class ImageOptim(BaseCompressTool):
    def __init__(self, command):
        self.command = command

    def compress(self, file_string):
        assert isinstance(super(ImageOptim, self).compress, object)
        super(ImageOptim, self).compress(file_string)
        command = self.command + " " + file_string
        old_size = os.path.getsize(file_string);
        os.popen(command).read()
        new_size = os.path.getsize(file_string);
        chg_size = long(old_size) - long(new_size)
        if chg_size > 0:
            return chg_size;
        else:
            return None
