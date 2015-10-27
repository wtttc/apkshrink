#! /usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import os
import sys

import mail_util
import Utils


def mail(out):
    mail_content = out
    subject = "..."
    email_from = "..."
    email_to = ["...", "...", "..."]
    user_name = "..."
    password = "..."
    SMPT_URL = "..."
    SMPT_PORT = 587
    mail_util.sendMail(mail_content, subject, email_from, email_to, user_name, password, SMPT_URL, SMPT_PORT, None)


def usage():
    print '------------compress.py usage:------------'
    print '-h, --help      : print help message.'
    print '-r, --res       : input res project floder path'
    print '----------------------------------------'


if __name__ == '__main__':
    res_floder = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:", ["help", "output="])

        # check all param
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage();
                sys.exit(1);
            if opt in ("-r", "--res"):
                res_floder = arg

    except getopt.GetoptError, e:
        print("getopt error! " + e.msg);
        exit()

    if res_floder is None:
        out = "res floder get None"
        mail(out)
        sys.exit(1);

    out = "res_floder:" + res_floder + "\n"

    RES_FLODER = res_floder + os.path.sep + "res"
    IMAGE_OPTIM_PATH = Utils.cur_file_dir() + os.path.sep + "ImageOptim.app"
    COMPARE_DICT = res_floder + os.path.sep + "build-tools" + os.path.sep + "res_pic_dict"
    WHITE_LIST_FILE = res_floder + os.path.sep + "build-tools" + os.path.sep + "res_compress_white_list"
    OUT_TEMP_FLODER = res_floder + os.path.sep + "bin"

    command = "python CompressChangedPic.py -r %s -t %s -d %s -o %s -w %s" % (
        RES_FLODER, IMAGE_OPTIM_PATH, COMPARE_DICT, OUT_TEMP_FLODER, WHITE_LIST_FILE)

    print("RES_FLODER:" + RES_FLODER)
    print("IMAGE_OPTIM_PATH:" + IMAGE_OPTIM_PATH)
    print("COMPARE_DICT:" + COMPARE_DICT)
    print("WHITE_LIST_FILE:" + WHITE_LIST_FILE)
    print("OUT_TEMP_FLODER:" + OUT_TEMP_FLODER)

    success = 0
    try:
        out += os.popen(command).read()
    except Exception, e:
        out += e.message
        success = 1

    print(out)
    mail(out)
    sys.exit(success)
