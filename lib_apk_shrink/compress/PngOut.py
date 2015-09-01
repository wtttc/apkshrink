#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tiantong'
import os
import re

from lib_apk_shrink.compress.BaseCompressTool import BaseCompressTool


# pngout [file path]
class PngOut(BaseCompressTool):
    def __init__(self, command):
        self.command = command

    def compress(self, file_string):
        assert isinstance(super(PngOut, self).compress, object)
        super(PngOut, self).compress(file_string)
        command = self.command + " " + file_string
        result = os.popen(command).read()
        if "Chg:" in result:
            # In:开头,有几个空格后跟着数字,到结尾前有任意字符，bytes结尾
            in_size_state = re.search(
                r'\bIn\b\:\s{1,8}\d+(.*?)bytes', result).group()
            # Chg:开头，后跟有任意字符，original)结尾
            chg_size_state = re.search(
                r'\bChg\b\:(.*?)original\)', result).group()
            # chgSizeState中，"-"开头的数字，去除"-"到结尾(整个数字段)
            chg_size = re.search(r'\-\d+', chg_size_state).group()[1:]
            # 压缩值累加
            return chg_size
        else:
            return None
