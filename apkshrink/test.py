#! /usr/bin/env python
# -*- coding: utf-8 -*-

# searchDict = dict()
# filename = "card_pic_item_layout"
# searchDict[filename] = 0
# file_path = "/Users/easytang/Documents/SVN/weibo5.1.2_mf_lite/weibo_dev_res/res/layout/act_pic_crop.xml"  # 输出文件路径信息
# file_object = open(file_path)
# file_content = file_object.read()  # 获得当前文件的内容
# search_string = '"@layout/card_pic_item_layout"'
# searchDict[filename] += file_content.count(search_string)  # 更新每个图片的引用次数
# print("searchDict:" + str(searchDict))
# file_object.close();
import os

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(path + " is removed")

file = open("UselessDrawable.txt")
dirname = "/Users/easytang/Documents/SVN/weibo5.1.2_mf_lite_3/weibo_dev_res/res"
while 1:
    lines = file.readlines(100000)
    if not lines:
        break
    for line in lines:
        filename1 = line[:-1] + '.xml'
        filename2 = line[:-1] + '.9.png'
        filename3 = line[:-1] + '.png'
        # print(filename)
        for p, d, f in os.walk(dirname):
            for sd in d:
                if "drawable" not in sd:
                    continue
                path = os.path.join(p, sd, filename1)
                remove_file(path)
                path = os.path.join(p, sd, filename2)
                remove_file(path)
                path = os.path.join(p, sd, filename3)
                remove_file(path)

