# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 18:17:50 2017

@author: xcsliu
"""
import requests
import pandas as pd
import json

timeout = 5
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
city_name = '北京'

city_url_pattern = 'http://restapi.amap.com/v3/config/district?key=89274958783f4fab44a2e3dba256dee0&keywords={}&subdistrict=2&extensions=all'
city_url = city_url_pattern.format(city_name)

# 用于将 polyline 转换成为 list of list 的形式 
def convert_str_ployline_to_json_format(polyline):
    test_json_polyline = '[[{}]]'.format(polyline)
    test_json_polyline = test_json_polyline.replace(';','],[')
    return test_json_polyline


# 返回城市下第一级列表
response = requests.get(city_url, headers=HEADERS, timeout=timeout)
text = response.text
text_json = json.loads(text)

# 城市一级行政区
city_detail_info = text_json['districts'][0]
city_polyline = convert_str_ployline_to_json_format(city_detail_info['polyline'])

# 城市下一级行政区
son_district_info = city_detail_info['districts'][0]
son_district_polyline = convert_str_ployline_to_json_format(son_district_info['polyline'])

# 城市下下一级行政区(对一线城市，比如上海适用)
grandson_district_name = []
for district in son_district_info['districts']:
    grandson_district_name.append(district['name'])



# 获得城市下一级行政区list
district_name_list_in_city = []
for district in districts['districts']:
    district_name_list_in_city.append(district['name'])



district_polyline_list = []    
pattern_url = 'http://restapi.amap.com/v3/config/district?key=89274958783f4fab44a2e3dba256dee0&keywords={}&subdistrict=2&extensions=all'
for district_name in district_name_list_in_city:
    district_url = pattern_url.format(district_name)
    response = requests.get(district_url, headers=HEADERS, timeout=timeout)
    text = response.text
    text_json = json.loads(text)
    
    
    districts = text_json['districts'][0]
    district_polyline = districts['polyline']
    json_format_district_polyline = convert_str_ployline_to_json_format(district_polyline)
    district_polyline_list.append(json_format_district_polyline)
    
    
df_city = pd.DataFrame(columns=['district_name','district_polyline'])
df_city['district_name'] = district_name_list_in_city
df_city['district_polyline'] = district_polyline_list

df_city['city_name'] = city_name
df_city['city_polyline'] = city_polyline


