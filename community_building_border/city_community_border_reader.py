# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 15:22:54 2017

@author: xcsliu
"""
import time
import pandas as pd
import requests
import json
import re
# import matplotlib.pyplot as plt

city_name = 'guangzhou'
read_file_path = 'E:\\PycharmPrjects\\playground\\poi_data\\2017_09_01\\{}\\ready_data\\{}_baidu_poi_2017_09_01.tsv'.format(city_name, city_name )
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

'''
geo_list = []
start = time.clock()
for idx,uid in enumerate(raw_data['uid'][len(geo_list):]):
    url_lunkuo_pattern = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&uid={}&ext_ver=new&l=12'
    url = url_lunkuo_pattern.format(uid)
    res = requests.get(url,timeout=5)
    text = res.text
    res= json.loads(text)
    geo = res['content']['geo']     
    geo_list.append(geo)
    print (idx)

end = time.clock()
print('运行时间：%-.2f s' % (end - start))

# ==============

尝试写一个循环，可以持续执行，直到 geo_list 收集完毕 
'''
geo_list = []
# raw_data = raw_data[:100]

def get_geo_list():
    try:
        for idx,uid in enumerate(raw_data['uid'][len(geo_list):]):
            url_lunkuo_pattern = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&uid={}&ext_ver=new&l=12'
            url = url_lunkuo_pattern.format(uid)
            res = requests.get(url,timeout=5)
            text = res.text
            res= json.loads(text)
            geo = res['content']['geo']     
            geo_list.append(geo)
            print (idx)
    except:
        if len(geo_list) == len(raw_data['uid']):
            return
        else:
            get_geo_list()

get_geo_list()
# ==============
# 用于统计小区轮廓数量
num_geo = 0
for i in geo_list:
    if i != '':
        num_geo += 1
        
print (num_geo)

# ==============


pattern = re.compile('1-(.*?);')
processed_geo_list = []
for idx,geo in enumerate(geo_list):
    processed_geo = re.findall(pattern, geo)
    res = [raw_data['name'][idx]] + processed_geo
    processed_geo_list.append(res)



# =======================
points_list = []
transfer_url_pattern = 'http://api.map.baidu.com/geoconv/v1/?coords={}&from=6&to=5&ak=GEPiAH9zkDx5oy4K1Vj7Znw8zmbGhY0M'

num = 0
for idx,geo in enumerate(processed_geo_list[num:100]):
    print (idx)
    num += 1
    if len(geo) > 1:
        ready_geo = get_ready(geo[1])
        single_community_point_list = ready_geo.split(',')
        transfer_url = transfer_url_pattern.format(ready_geo)                     
        res = requests.get(transfer_url)
        text = res.text
        content = json.loads(text)      
        points = content['result']
        points_dumps = json.dumps(points)
        points_list.append([geo[0],points_dumps])
# =================================================        
#'''
num = 0
for idx,geo in enumerate(processed_geo_list[num:]):
    print (idx)
    num += 1
    if len(geo) > 1:
        ready_geo = get_ready(geo[1])
        single_community_point_list = ready_geo.split(',')
        if len(single_community_point_list) < 90:   
            transfer_url = transfer_url_pattern.format(ready_geo)                     
            res = requests.get(transfer_url)
            text = res.text
            content = json.loads(text)      
            points = content['result']
            points_dumps = json.dumps(points)
            points_list.append([geo[0],points_dumps])
        else:
            num_transfer = int( len(single_community_point_list)/90 )
            geo_list = [single_community_point_list[i*90:(i+1)*90] for i in range(num_transfer) ]+ [single_community_point_list[num_transfer*90:]]
            str_geo_list = [','.join(geo) for geo in geo_list]
            tmp_point_list = []
            for ready_geo in str_geo_list:
                transfer_url = transfer_url_pattern.format(ready_geo)                     
                res = requests.get(transfer_url)
                text = res.text
                content = json.loads(text)      
                points = content['result']
                tmp_point_list.extend(points)
            points_dumps = json.dumps(tmp_point_list)
            points_list.append([geo[0],points_dumps])            
#'''            
    

def get_date(format="%Y_%m_%d"):
    date = time.strftime(format, time.localtime())
    return date

'''
date = get_date()

save_file_path = 'E:\\building_processed_data\\{}_community_border_{}.tsv'.format(city_name, date)

points_list_pd = pd.DataFrame(points_list)

points_list_pd.to_csv(path_or_buf=save_file_path, sep='\t', encoding='utf-8')

# =====================
# test plot
''' 

for idx,i in enumerate(processed_geo_list):
    if i[0] == '广州雅居乐花园':
        print (idx)

print ( processed_geo_list[16244] )
data = processed_geo_list[16244][1]

d = data.split(',')

split_num = 50
single_community_point_list = data.split(';')
num_transfer = int( len(single_community_point_list)/split_num )
geo_list = [single_community_point_list[i*split_num:(i+1)*split_num] for i in range(num_transfer) ]+ [single_community_point_list[num_transfer*split_num:]]
str_geo_list = [';'.join(geo) for geo in geo_list]    


tmp_point_list = []
p = []

for ready_geo in str_geo_list:
    transfer_url = transfer_url_pattern.format(ready_geo)                     
    res = requests.get(transfer_url)
    text = res.text
    content = json.loads(text)      
    points = content['result']
    tmp_point_list.extend(points)
points_dumps = json.dumps(tmp_point_list)
p.append([geo[0],points_dumps])  

ready_geo = str_geo_list[0]
test_url = transfer_url_pattern.format('12560424.6456,2626547.86716,12560436.4585,2626555.06146,12560536.3017,2626442.42048,12560457.7071,2626376.86362,12560446.6463,2626409.25986,12560433.2049,2626457.62755,12560424.7741,2626497.43379,12560424.6456,2626547.86716')    
res = requests.get(test_url)
text = res.text
content = json.loads(text)      
points = content['result']

















