#! /bin/sh
cd /home/xkool/venv/poi
echo "enter virtual env"
. ./bin/activate

echo "crawling anjuke"
/home/xkool/venv/poi/bin/python3 /home/xkool/poi/crawler/anjuke_crawler.py

