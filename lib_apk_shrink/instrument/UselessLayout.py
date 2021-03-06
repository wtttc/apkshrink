#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from lib_apk_shrink.model.UselessLayoutConfig import UselessLayoutConfig

__author__ = 'tiantong'

from lib_apk_shrink.log.Logger import Logger

log = Logger(logname='UselessLayout.txt', loglevel=0, logger="UselessLayout", hasformat=False).getlog()

FILE_JAVA_OWN = 0
FILE_JAVA_THIRDPARTY = 1
FILE_XML_NORMAL = 2
FILE_XML_WITH_QUOTE = 3


class UselessLayout(object):
    useless_layout_config = UselessLayoutConfig()
    layout_dict = dict()
    extra_jar_path = None
    fast_search = False;

    def __init__(self, uselessLayoutConfig=UselessLayoutConfig()):
        self.useless_layout_config = uselessLayoutConfig

    def check_useless_layout(self):
        layout_dirs = self.useless_layout_config.layout_dir
        for dir in layout_dirs:
            # 初始化layout_set
            for filename in os.listdir(dir):
                raw_name = filename.split(".")[0].encode("utf-8")
                if 'xml' in filename:
                    self.layout_dict[raw_name] = 0
        print ""
        print "raw:"
        print self.layout_dict

        for dir in layout_dirs:
            self.find_dict_in_rootpath(dir, self.layout_dict, FILE_XML_WITH_QUOTE)
        print ""
        print "after search layout:"
        print self.layout_dict

        xml_dirs = self.useless_layout_config.xml_dir
        for dir in xml_dirs:
            self.find_dict_in_rootpath(dir, self.layout_dict, FILE_XML_NORMAL)
        print ""
        print "after search xml dirs:"
        print self.layout_dict

        src_dirs = self.useless_layout_config.src_dir
        for dir in src_dirs:
            self.find_dict_in_rootpath(dir, self.layout_dict, FILE_JAVA_OWN)
        print ""
        print "after search src:"
        print self.layout_dict

        if self.extra_jar_path is not None:
            self.find_dict_in_rootpath(self.extra_jar_path, self.layout_dict, FILE_JAVA_THIRDPARTY)
        print ""
        print "after search extra_jar_path:"
        print self.layout_dict

    # 查找指定dict 在指定 文件夹下的匹配次数
    # rootpath：要查找的文件夹路径
    # set： 要查找的文件名set
    def find_dict_in_rootpath(self, rootpath, dict, file_type=FILE_JAVA_OWN):
        for parent, dirnames, filenames in os.walk(rootpath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:  # 输出文件信息
                if "svn-base" in filename:
                    # 过滤svn文件
                    continue
                file_path = os.path.join(parent, filename)  # 输出文件路径信息
                file_object = open(file_path)
                file_content = file_object.read()  # 获得当前文件的内容
                print("filename:" + filename)
                for pic_name in dict.keys():
                    if self.fast_search and dict[pic_name] > 0:
                        # 已经查到的就不在搜索
                        continue
                    search_string = pic_name
                    if file_type == FILE_XML_NORMAL:
                        search_string = '@layout/' + search_string
                        # print("filename:" + filename + " search_string:" + search_string)
                        count = file_content.count(search_string)
                        # print("count:" + str(count))
                        dict[pic_name] += count  # 更新每个图片的引用次数
                    elif file_type == FILE_XML_WITH_QUOTE:
                        # 检查layout xml的方式主要寻找 include viewStub的方式
                        # 引号也要查找，避免碰到前缀一样的 如:"main"&"main_layout"
                        search_string = '"@layout/' + search_string + '"'
                        # print("filename:" + filename + " search_string:" + search_string)
                        count = file_content.count(search_string)
                        # print("count:" + str(count))
                        dict[pic_name] += count  # 更新每个图片的引用次数
                    elif file_type == FILE_JAVA_OWN:
                        # TODO 有部分代码使用了getIdentifier方法，比较蛋疼
                        search_string = 'R.layout.' + search_string + r'[;|)|,|\s]'
                        # if not self.fast_search:
                        #     search_string1 = search_string1 + '|getIdentifier.*' + search_string
                        sp1 = re.findall(search_string, file_content)
                        count = len(sp1)
                        # print("filename:" + filename + " search_string:" + search_string)
                        # print("count:" + str(count))
                        # count = file_content.count(search_string)
                        if count > 0:
                            dict[pic_name] += count  # 更新每个图片的引用次数
                    elif file_type == FILE_JAVA_THIRDPARTY:
                        count = file_content.count(search_string)
                        # sp = re.findall(search_string, file_content)
                        # count = len(sp)
                        # print("filename:" + filename + " search_string:" + search_string)
                        # print("count:" + str(count))
                        if count > 0:
                            dict[pic_name] += count  # 更新每个图片的引用次数
                file_object.close();

    def writeResult(self):
        for pic_name in self.layout_dict.keys():
            if self.layout_dict[pic_name] == 0:
                log.info(pic_name)

    def deleteUseless(self):
        layout_dirs = self.useless_layout_config.layout_dir
        for d, x in self.layout_dict.items():
            if x == 0:
                ignore = False
                for filter in self.useless_layout_config.white_list:
                    if filter in str(d):
                        ignore = True

                if ignore:
                    print("file:" + str(d) + " is in white list")
                    continue

                for dir in layout_dirs:
                    path = os.path.join(dir, str(d) + '.xml')
                    print(path)
                    if os.path.isfile(path):
                        os.remove(path)
