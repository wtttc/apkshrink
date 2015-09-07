#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re

__author__ = 'tiantong'
import os

from lib_apk_shrink.model.UselessDrawableConfig import UselessDrawableConfig
from lib_apk_shrink.log.Logger import Logger

log = Logger(logname='UselessDrawable.txt', loglevel=0, logger="UselessDrawable", hasformat=False).getlog()

res_file_type = ["xml", "png", "jpg", "jpeg", "bmp"]


class UselessDrawable(object):
    useless_drawable_config = UselessDrawableConfig()
    drawable_dict = dict()
    extra_jar_path = None
    fast_search = False

    def __init__(self, uselessDrawbaleConfig=UselessDrawableConfig()):
        self.useless_drawable_config = uselessDrawbaleConfig

    def check_useless_drawable(self):
        res_dir = self.useless_drawable_config.res_dir
        for dir in res_dir:
            for sparent, sdirnames, sfilenames in os.walk(dir):
                for dirname in sdirnames:
                    if "drawable" not in dirname:
                        continue
                    path_dir = os.path.join(sparent, dirname)
                    for parent, dirnames, filenames in os.walk(path_dir):
                        for filename in filenames:
                            file_type = filename.split(".")[-1]
                            raw_name = filename.split(".")[0].encode("utf-8")
                            # print "filetype:" + file_type + " raw_name:" + raw_name
                            if file_type in res_file_type:
                                self.drawable_dict[raw_name] = 0

        print ""
        print "raw:"
        print self.drawable_dict

        # src中搜寻
        src_dirs = self.useless_drawable_config.src_dir
        for dir in src_dirs:
            self.find_dict_in_rootpath(dir, self.drawable_dict)
        print ""
        print "after search src:"
        print self.drawable_dict

        # extra_jar_path中搜寻
        if self.extra_jar_path is not None:
            self.find_dict_in_rootpath(self.extra_jar_path, self.drawable_dict)
        print ""
        print "after search extra_jar_path:"
        print self.drawable_dict

        res_dir = self.useless_drawable_config.res_dir
        for dir in res_dir:
            self.find_dict_in_res(dir, self.drawable_dict)
        print ""
        print "after search res_dir:"
        print self.drawable_dict

        extra_xml = self.useless_drawable_config.extra_xml
        for extra_one in extra_xml:
            # print(extra_one)
            self.find_dict_in_xml_file(extra_one, self.drawable_dict, True)
        print ""
        print "after search extra_xml:"
        print self.drawable_dict

    # 查找指定dict 在指定 文件夹下的匹配次数
    # rootpath：要查找的文件夹路径
    # set： 要查找的文件名set
    def find_dict_in_rootpath(self, rootpath, dict):
        for parent, dirnames, filenames in os.walk(rootpath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:  # 输出文件信息
                if "svn-base" in filename:
                    # 过滤svn文件
                    continue
                file_path = os.path.join(parent, filename)  # 输出文件路径信息
                file_object = open(file_path)
                file_content = file_object.read()  # 获得当前文件的内容
                for pic_name in dict.keys():
                    if self.fast_search and dict[pic_name] > 0:
                        # 已经查到的就不在搜索
                        continue
                    search_string = pic_name
                    # R.layout.xxx 结尾是 空格 ) ;
                    # TODO 注释中的还会搜出来
                    search_string = 'R.drawable.' + search_string + r'[;|)|,|\s]'
                    sp = re.findall(search_string, file_content)
                    print("search_string:" + search_string)
                    print("filename:" + filename)
                    count = len(sp)
                    if count > 0:
                        dict[pic_name] += count  # 更新每个图片的引用次数
                file_object.close();

    def find_dict_in_res(self, rootpath, dict):
        for parent, dirnames, filenames in os.walk(rootpath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:  # 输出文件信息
                # 检查出xml文件 layout文件 xml定义drawable文件 style文件 xml配置文件
                if "xml" not in filename:
                    continue;
                file_path = os.path.join(parent, filename)  # 输出文件路径信息
                self.find_dict_in_xml_file(file_path, dict)

    def find_dict_in_xml_file(self, file_path, dict, extra=False):
        file_object = open(file_path)
        file_content = file_object.read()  # 获得当前文件的内容
        for pic_name in dict.keys():
            if self.fast_search and dict[pic_name] > 0:
                # 已经查到的就不在搜索
                continue
            search_string = pic_name
            # 检查layout xml的方式主要寻找 include viewStub的方式
            # 引号也要查找，避免碰到前缀一样的 如:"main"&"main_layout"
            # TODO XML中解析DOM获取已经引用的drawable
            if extra:
                search_string = '@drawable/' + search_string
            else:
                search_string = '"@drawable/' + search_string + '"'
            dict[pic_name] += file_content.count(search_string)  # 更新每个图片的引用次数
        file_object.close();

    def writeResult(self):
        for pic_name in self.drawable_dict.keys():
            if self.drawable_dict[pic_name] == 0:
                # print(pic_name)
                log.info(pic_name)
