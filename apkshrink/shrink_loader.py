#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 从配置文件中读取压缩设置
import json

from lib_apk_shrink.model import CompressConfig,  CompressState, WebPConfig, \
    DecompileConfig, UselessLayoutConfig, UselessDrawableConfig
from lib_apk_shrink.utils import shrink_utils


def init_compress_config(file_path):
    _json = shrink_utils.get_json_from_file(file_path)
    _compress_config = CompressConfig.CompressConfig(_json)
    return _compress_config


# 从配置文件获取压缩状态
def init_compress_state(file_path):
    _json = shrink_utils.get_json_from_file(file_path)
    _compress_state = CompressState.CompressState(_json)
    return _compress_state


# 从配置文件中读取webP转换配置
def init_webp_config(file_path):
    _json = shrink_utils.get_json_from_file(file_path)
    _webp_config = WebPConfig.WebPConfig(_json)
    return _webp_config


def init_useless_layout_config(file_path):
    _json = shrink_utils.get_json_from_file(file_path)
    _useless_layout_config = UselessLayoutConfig.UselessLayoutConfig(_json)
    return _useless_layout_config


def init_decompile_config(file_path):
    _json = shrink_utils.get_json_from_file(file_path)
    _decompile_config = DecompileConfig.DecompileConfig(_json)
    return _decompile_config


def init_useless_drawbale_config(file_path):
    _json = shrink_utils.get_json_from_file(file_path)
    _useless_layout_config = UselessDrawableConfig.UselessDrawableConfig(_json)
    return _useless_layout_config


# 将compressState写入文件
def write_compress_state(file_dir, compress_state):
    try:
        output_s = open(file_dir, 'w+')
        output = json.dumps(
            compress_state.__dict__, ensure_ascii=False, indent=4, sort_keys=True)
        output_s.write(output)
        output_s.flush()
    except Exception, e:
        print e
        exit()
