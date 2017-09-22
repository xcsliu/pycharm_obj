# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 16:10:58 2017

@author: xcsliu
重庆：
106.53063501341296 29.54460610888615



TIMEOUT = 5
STEP_NUM = 10
UNIT_DISTANCE = 0.005
THREAD_NUM = 30
所以是长宽各是 0.05 个经纬度
左下：106.52563501341296 29.53960610888615
右上：106.53563501341296 29.54960610888615

#选择表格中的'w'列，返回的是DataFrame类型
data[['w']]  

#选择表格中的'w'、'z'列
data[['w','z']]  

#返回第1行到第2行的所有行，前闭后开，包括前不包括后
data[0:2] 
 
#返回第2行，从0计，返回的是单行，通过有前后值的索引形式，
data[1:2] 
 
       #如果采用data[1]则报错

"""
import pandas as pd

read_file_path_1 = 'E:\\PycharmPrjects\\poi\\poi\\poi_data\\2017_09_05\\chongqing\\raw_data\\chongqing_fangtianxia_parcel_2017_09_05.tsv'
read_file_path_2 = 'E:\\PycharmPrjects\\poi\\poi\\poi_data\\2017_09_05\\chongqing\\ready_data\\chongqing_anjuke_second_hand_community_2017_09_05.tsv'


ready_data_new = pd.read_table(read_file_path_1, error_bad_lines=False)
ready_data_old = pd.read_table(read_file_path_2, error_bad_lines=False)

a = ready_data_old[ready_data_old['truncate_name']=='雍江翠湖']


lats = ready_data_old[ready_data_old['lat']<29.544]
print (lats[0:1]['lat'])


import requests
BAIDU_API_AK = '0yMQoetZ3YOogQyAjr7CcUPBzCT82yBp'
street_view_url_pattern = '  http://api.map.baidu.com/panorama/v2?ak={}&width=512&height=256&location={},{}&fov=180'

lng = str(a['lng'][0])
lat = str(a['lat'][0])
url = street_view_url_pattern.format(BAIDU_API_AK,lng,lat)

res = requests.get(url)
text = res.text










