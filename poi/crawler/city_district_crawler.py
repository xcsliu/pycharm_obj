# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 19:03:14 2017

@author: xcsliu
"""
import requests
import pandas as pd
import json
from pypinyin import lazy_pinyin
from shapely.geometry import Polygon, Point


class CityDistrictCrawler:
    def __init__(self, city_name):
        self.timeout = 5
        self.HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
        self.city_name = city_name
        
        self.district_url_pattern = 'http://restapi.amap.com/v3/config/district?key=89274958783f4fab44a2e3dba256dee0&keywords={}&subdistrict=2&extensions=all'
        self.city_url = self.district_url_pattern.format(city_name)
        
        
    def convert_str_ployline_to_json_format(self, polyline):
        test_json_polyline = '[[{}]]'.format(polyline)
        test_json_polyline = test_json_polyline.replace(';','],[')
        return test_json_polyline      


    def get_city_polyline_and_district_list(self):
        response = requests.get(self.city_url, headers=self.HEADERS, timeout=self.timeout)
        text = response.text
        text_json = json.loads(text)
        districts = text_json['districts'][0]
        city_polyline = self.convert_str_ployline_to_json_format(districts['polyline'])
        
        district_name_list_in_city = []
        for district in districts['districts']:
            district_name_list_in_city.append(district['name'])
    
        return city_polyline, district_name_list_in_city


    def get_district_polyline_list(self, district_name_list_in_city):
        district_polyline_list = []  
        for district_name in district_name_list_in_city:
            district_url = self.district_url_pattern.format(district_name)
            response = requests.get(district_url, headers=self.HEADERS, timeout=self.timeout)
            text = response.text
            text_json = json.loads(text)

            districts = text_json['districts'][0]
            district_polyline = districts['polyline']
            json_format_district_polyline = self.convert_str_ployline_to_json_format(district_polyline)
            district_polyline_list.append(json_format_district_polyline)
        return district_polyline_list


    def save_file(self):
        city_polyline, district_name_list_in_city = self.get_city_polyline_and_district_list()
        district_polyline_list = self.get_district_polyline_list(district_name_list_in_city)
        
        # 检测该district中心点是否在该城市范围内：
        
        
        
        df_city = pd.DataFrame(columns=['district_name','district_polyline'])
        df_city['district_name'] = district_name_list_in_city
        df_city['district_polyline'] = district_polyline_list  
        df_city['city_name'] = self.city_name
        df_city['city_polyline'] = city_polyline


        city_name_pinyin = ''.join(lazy_pinyin(self.city_name))
        file_path_pattern = 'E:\\xcsliu_project\\pycharm_obj\\city_district_polylines\\{}.tsv'
        file_path = file_path_pattern.format(city_name_pinyin)
        df_city.to_csv(path_or_buf=file_path, sep='\t', index=False)


# =======================

def get_city_name_list():
    # 标准城市列表
    read_file_path = 'E:\\poi_data\\cities.tsv'
    city_list = pd.read_table(read_file_path, error_bad_lines=False, header = None, names = ['a','b','c','d','e','f','g','h','i','j','k','l'])    
    a = city_list[city_list['c'] == 1] 
    
    c_list = []
    for idx, row in a.iterrows():
        if row['g'] == '直辖县':
            continue
        elif row['g'] != '直辖区':
            city = row['g']
        else:
            city = row['h'] + '市'
            
        city_name = city.replace('臺','台')
        c_list.append(city_name)
            
            
    city_list = c_list[:338]+c_list[344:]
    return city_list

city_list = get_city_name_list()



saved_list = []
city_list = get_city_name_list()


for index, city in enumerate(city_list):
    if city not in saved_list:
        crawler = CityDistrictCrawler(city)
        print (index, city)
        crawler.save_file()
        saved_list.append(city)
    else:
        pass
    
unsaved_list = [k for k in city_list if k not in saved_list]
print (unsaved_list)




'①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'