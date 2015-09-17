#! /usr/bin/env python
# -*- coding: utf-8 -*-
from lib_apk_shrink.utils import shrink_utils

__author__ = 'tiantong'
import os
import re

from lib_apk_shrink.compress.BaseCompressTool import BaseCompressTool


# SingleShrink [file path]
class SingleShrink(BaseCompressTool):
    def __init__(self, command):
        self.command = command

    def compress(self, file_string):
        assert isinstance(super(SingleShrink, self).compress, object)
        super(SingleShrink, self).compress(file_string)
        command = self.command + " " + file_string
        result = os.popen(command).read()
        old_size = shrink_utils.get_path_size(file_string);
        os.popen(command).read()
        new_size = shrink_utils.get_path_size(file_string);
        chg_size = long(old_size) - long(new_size)
        return chg_size;
