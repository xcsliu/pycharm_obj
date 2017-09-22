# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 10:56:19 2017

import matplotlib.pyplot as plt
fig, axs = plt.subplots()
for p in points:
    xs, ys = p[0], p[1]
axs.plot(xs, ys)
plt.show()
@author: xcsliu
"""
import pandas as pd
import requests
import json
import re
import matplotlib.pyplot as plt


read_file_path = 'E:\\PycharmPrjects\\playground\\poi_data\\2017_09_01\\chongqing\\ready_data\\chongqing_baidu_poi_2017_09_01.tsv'
raw_data = pd.read_table(read_file_path, error_bad_lines=False)


def get_ready(strs):
    num = 0
    new_strs = []
    for i in strs:
        if i == ',' and num & 1 == 1:
            new_strs.append(';')
            num += 1
        elif i == ',':
            new_strs.append(',')
            num += 1            
        else:
            new_strs.append(i)  
    return ''.join(new_strs)


geo_list = []
for uid in raw_data['uid']:
    url_lunkuo_pattern = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&uid={}&ext_ver=new&l=12'
    url = url_lunkuo_pattern.format(uid)
    res = requests.get(url)
    text = res.text
    res= json.loads(text)
    geo = res['content']['geo']     
    geo_list.append(geo)


url_lunkuo_pattern = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&uid={}&ext_ver=new&l=12'
url = url_lunkuo_pattern.format(uid)
res = requests.get(url)
text = res.text
content = json.loads(text)

num_geo = 0
for i in geo_list:
    if i != '':
        num_geo += 1
        
print (num_geo)



pattern = re.compile('1-(.*?);')
processed_geo_list = []
for idx,geo in enumerate(geo_list):
    processed_geo = re.findall(pattern, geo)
    res = [raw_data['name'][idx]] + processed_geo
    processed_geo_list.append(res)
        
b = get_ready(processed_geo_list[30][1])  
# =================
transfer_url_pattern = 'http://api.map.baidu.com/geoconv/v1/?coords={}&from=6&to=5&ak=GEPiAH9zkDx5oy4K1Vj7Znw8zmbGhY0M'
transfer_url = transfer_url_pattern.format(b)                     
res = requests.get(transfer_url)
text = res.text
content = json.loads(text)      

points = content['result']            

# ==============

x=[]
y=[]
for i in points:
    x.append(i['x'])
    y.append(i['y'])

##    plt.fill(x,y,'b')
plt.plot(x,y,'b-', linewidth=2)
plt.show()   
        