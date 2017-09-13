#!/bin/sh
cd /home/xkool/venv/poi
echo "enter virtual env"
. ./bin/activate

echo "crawling baidu"
/home/xkool/venv/poi/bin/python3 /home/xkool/poi/crawler/baidu_crawler.py

