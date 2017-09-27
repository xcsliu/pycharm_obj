"""
Created on Mon Sep 25 10:19:24 2017

@author: xcsliu
city pic for ppt
"""
import requests
import re
import pandas as pd
from pypinyin import lazy_pinyin

timeout = 5
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}


city_name = '无锡'
pattern_url = 'https://baike.baidu.com/item/{}'
url = pattern_url.format(city_name)
response = requests.get(url, headers=HEADERS, timeout=timeout)
text = response.text

t = text.encode('ISO-8859-1').decode('utf8')

# ====
pattern_all = re.compile('<img src="(https://gss.*?)" />')
res_all = re.findall(pattern_all, t)
# 单独选择图集的首页
pattern_1 = re.compile('<img src="(.*?)" />[.\n]*?<button class="picAlbumBtn">')
res_1 = re.findall(pattern_1, t)


# ====
# 处理城市列表：

read_file_path = 'E:\\poi_data\\cities.tsv'
city_list = pd.read_table(read_file_path, error_bad_lines=False, header = None, names = ['a','b','c','d','e','f','g','h','i','j','k','l'])

a = city_list[city_list['c'] == 1]
dd = list(a['h'].drop_duplicates())


c_list = []
for idx, row in a.iterrows():
    if row['g'] == '直辖县':
        continue
    elif row['g'] != '直辖区':
        city = row['g']
        c_list.append(city)
    else:
        city = row['h'] + '市'
        c_list.append(city)


d = list(c_list.drop_duplicates())


import urllib

# 网络上图片的地址
img_src = res_1[0]

# 将远程数据下载到本地，第二个参数就是要保存到本地的文件名
city_name_pinyin = ''.join(lazy_pinyin(city_name))

path_pic_pattern = 'E:\\xcsliu_project\\pycharm_obj\\city_pic_data\\{}.jpg'
path_pic = path_pic_pattern.format(city_name_pinyin)
urllib.request.urlretrieve(img_src, path_pic)


