#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tiantong'

# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
import logging


class Logger():
    def __init__(self, logname, loglevel, logger, hasformat=True):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        if hasformat:
            # 定义handler的输出格式
            formatter = logging.Formatter('[%(asctime)s %(name)s]-%(levelname)s- %(message)s')
            # formatter = format_dict[int(loglevel)]
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger
