#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import mail_util

RES_FLODER = ".../res"
IMAGE_OPTIM_PATH = ".../ImageOptim.app"
COMPARE_DICT = ".../res_pic_dict"
WHITE_LIST_FILE = ".../res_compress_white_list"
OUT_TEMP_FLODER = ".../bin"

command = "python CompressChangedPic.py -r %s -t %s -d %s -o %s -w %s" % (
    RES_FLODER, IMAGE_OPTIM_PATH, COMPARE_DICT, OUT_TEMP_FLODER, WHITE_LIST_FILE)


def mail(out):
    mail_content = out
    email_from = "..."
    email_to = ["..."]
    user_name = "..."
    password = "..."
    SMPT_URL = "..."
    SMPT_PORT = 587
    mail_util.sendMail(mail_content, email_from, email_to, user_name, password, SMPT_URL, SMPT_PORT, None)


if __name__ == '__main__':
    success = 0
    try:
        out = os.popen(command).read()
    except Exception, e:
        out = e.message
        success = 1

    print(out)
    mail(out)
    sys.exit(success)
