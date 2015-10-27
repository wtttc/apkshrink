#!/usr/bin/env bash
python compress.py -r .../weibo_dev_res_git

if [ $?==0 ]
then
    echo "compressed success"
else
    echo "compressed failed"
fi