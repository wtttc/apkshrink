#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys

__author__ = 'tiantong'


def walk_dir(folder, method, output_dir):
    for parent, dirnames, filenames in os.walk(folder):
        for dirname in dirnames:
            # 过滤掉非drawable的目录
            if "drawable" in dirname:
                folder_path = os.path.join(parent, dirname)
                print ("")
                print (folder_path)
                for s_parent, s_dirnames, s_filenames in os.walk(folder_path):
                    walk_pic_valid(dirname, s_filenames, output_dir, method)


def crunch_compress(in_string, out_string):
    command = aapt_path
    exc_command = command + " c -v -S " + in_string + " -C " + out_string
    print("exc_command:" + exc_command)
    result = os.popen(exc_command).read()
    print result


def walk_pic_valid(dirname, filenames, output_dir, process_method):
    for filename in filenames:
        # 过滤图片文件
        if filename.split('.')[-1] not in ['.jpg', '.jpeg', '.gif', 'png', 'bmp']:
            continue
        # 确认输入输出路径
        in_string = os.path.join(input_folder, dirname, filename)
        print("in_string:" + in_string)
        out_string = os.path.join(output_dir, dirname, filename)
        print("out_string:" + out_string)

        # 保证输出文件夹存在
        cur_dir = os.path.join(output_dir, dirname)
        # 保证res存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # 保证指定drawable文件夹存在
        if not os.path.exists(cur_dir):
            os.makedirs(cur_dir)

        # 处理图片
        process_method(dirname, filename, in_string, out_string)


def do_9_patch_pic(dirname, filename, in_string, out_string):
    if ".9." in filename:
        print ("find 9 patch in " + dirname + " file " + filename)
        if os.path.exists(in_string) and not os.path.exists(out_string):
            shutil.copy(in_string, out_string)


def do_normal_pic(dirname, filename, in_string, out_string):
    if ".9." in filename:
        pass
    else:
        print ("find normal in " + dirname + " file " + filename)
        if os.path.exists(in_string) and not os.path.exists(out_string):
            shutil.copy(in_string, out_string)

# print 'Argument List:', str(sys.argv)
# print sys.argv[1]
# arg1 -> input 文件夹 需要压缩的res文件夹绝对路径
# arg2 -> onput 文件夹 输出res文件夹绝对路径
# arg2 -> aapt 指令绝对路径

input_folder = sys.argv[1]
output_folder = sys.argv[2]
aapt_path = sys.argv[3]
res_9_raw_dir = os.path.join(output_folder, "res_9_raw")
res_dir = os.path.join(output_folder, "res")
print('input_folder:' + input_folder)
print('output_folder:' + output_folder)
print('aapt_path:' + aapt_path)
print("res_9_raw_dir:" + res_9_raw_dir)
print("res_dir:" + res_dir)

# 复制.9图到res_9_raw_dir
walk_dir(input_folder, do_9_patch_pic, res_9_raw_dir)
# crunch res_9_raw_dir下地.9图到res_dir中
crunch_compress(res_9_raw_dir, res_dir)
# 复制普通的图片到9图到res_dir中
walk_dir(input_folder, do_normal_pic, res_dir)


# <target name="-crunch" >
#   <exec executable="python"
#   taskName="crunch">
#   <arg value="compress_9_patch.py"/>
#   <arg value="${project.lib.res}/res"/>
#   <arg value="${out.dir}" />
#   <arg value="${android.build.tools.dir}/aapt${exe}" />
#   </exec>
# </target>
