#! /usr/bin/env python
# -*- coding: utf-8 -*-
from lib_apk_shrink.utils import shrink_utils

__author__ = 'tiantong'
import os

from lib_apk_shrink.compress.BaseCompressTool import BaseCompressTool



# ImageOptim [file path]
# mac 版本没有命令行输出，不方便统计
class ImageOptim(BaseCompressTool):
    def __init__(self, command):
        self.command = command

    def compress(self, floder_string):
        assert isinstance(super(ImageOptim, self).compress, object)
        super(ImageOptim, self).compress(floder_string)
        command = self.command + " " + floder_string
        old_size = shrink_utils.get_path_size(floder_string);
        os.popen(command).read()
        new_size = shrink_utils.get_path_size(floder_string);
        chg_size = long(old_size) - long(new_size)
        if chg_size > 0:
            return chg_size;
        else:
            return None
