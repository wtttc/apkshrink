#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil

from lib_apk_shrink.model.DecompileConfig import DecompileConfig

__author__ = 'tiantong'


class JarDecompile(object):
    decompile_config = DecompileConfig()
    output_path_decompile = ""
    output_path_out = ""

    def __init__(self, decompileConfig=DecompileConfig()):
        self.decompile_config = decompileConfig

    def decompile_jar(self):
        jad_path = self.decompile_config.jad_path
        output_path = self.decompile_config.output_path

        # 删除以前的文件夹
        self.output_path_out = os.path.join(output_path, 'out')
        self.output_path_decompile = os.path.join(output_path, 'decompile')
        self.clearOutput();

        # 确保文件夹存在
        if not os.path.exists(self.output_path_out):
            os.makedirs(self.output_path_out)

        # 删除无用的 META-INF
        META_path = os.path.join(self.output_path_out, 'META-INF')

        # 解压jar
        for jar_path in self.decompile_config.extra_jar:
            command = 'unzip ' + jar_path + ' -d ' + self.output_path_out
            result = os.popen(command).read()
            self.delDir(META_path)


        # 反编译
        command = jad_path + ' -r -ff -o -d ' + self.output_path_decompile + ' -s java ' + self.output_path_out + '/**/*.class'
        result = os.popen(command).read()

    def delDir(self, dir):
        if os.path.isdir(dir):
            shutil.rmtree(dir)

    def clearOutput(self):
        self.delDir(self.output_path_decompile)
        self.delDir(self.output_path_out)
