#!/bin/sh
cd /home/xkool/venv/poi
echo "enter virtual env"
. ./bin/activate

echo "crawling anjuke"
/home/xkool/venv/poi/bin/python3 /home/xkool/poi/crawler/anjuke_crawler.py
echo "crawling lianjia"
/home/xkool/venv/poi/bin/python3 /home/xkool/poi/crawler/lianjia_crawler.py
echo "crawling baidu"
/home/xkool/venv/poi/bin/python3 /home/xkool/poi/crawler/baidu_crawler.py
echo "crawling fangtianxia"
/home/xkool/venv/poi/bin/python3 /home/xkool/poi/crawler/fangtianxia_crawler.py
deactivate
