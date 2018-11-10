#!/bin/sh -e
echo "start spider....."
nohup python start_spider.py > wenshu_log/wenshu_xingshi1.log 2>&1 &
