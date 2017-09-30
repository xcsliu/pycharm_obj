# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 16:25:52 2017

@author: xcsliu
"""


import pandas as pd
import json
from pypinyin import lazy_pinyin
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt



def get_city_dataframe_by_city_name(city_name):
    city_name_pinyin = ''.join(lazy_pinyin(city_name))
    file_path_pattern = 'E:\\xcsliu_project\\pycharm_obj\\city_district_polylines\\{}.tsv'
    file_path = file_path_pattern.format(city_name_pinyin)
    districts_pd = pd.read_table(file_path, error_bad_lines=False, encoding='gbk')    
    return districts_pd

def plot_single_district_by_district_polyline_strs(district_polyline_strs, district_name, ax):
    district_list = json.loads(district_polyline_strs)
    
    # 所有待画图的区块
    sub_districts_in = []
    for idx, i in enumerate(district_list):
        district_polygon = i
        tmp_x, tmp_y = [], []
        for k in district_polygon:
            tmp_x.append(k[0])
            tmp_y.append(k[1])
        sub_districts_in.append([tmp_x, tmp_y])    

    # 画出轮廓并且填充颜色
    for idx, sub_district in enumerate( sub_districts_in ):
        plt.plot(sub_district[0], sub_district[1], 'w-',linewidth=2)
        plt.fill(sub_district[0], sub_district[1], 'r', alpha=0.3)            
        
        
    # 计算中心点位置：
    center_point_x = 0
    center_point_y = 0
    sub_max_area = 0
    for idx, i in enumerate(district_list):
        district_polygon = i
        polygon_obj = Polygon(district_polygon)
        if polygon_obj.area > sub_max_area:
            center_point_x = list(polygon_obj.centroid.coords)[0][0]
            center_point_y = list(polygon_obj.centroid.coords)[0][1]
            sub_max_area = polygon_obj.area
    center_point = [center_point_x, center_point_y]

    # 标注行政区名称
    ax.annotate(district_name,   
                xy = (center_point[0]-0.05, center_point[1]), 
                xycoords='data',
                fontsize=12)    
 
    
    
def draw_pic_by_city_name(city_name):
    city_df = get_city_dataframe_by_city_name(city_name)
    
    # 画布初始化
    plt.rcParams['font.sans-serif']=['SimHei']
    fig = plt.figure(0)
    fig.set_size_inches(12, 12)
    ax = fig.add_subplot(111)
    
    for idx, row in city_df.iterrows():
        district_name = row['district_name']
        district_polyline_strs = row['district_polyline']
        plot_single_district_by_district_polyline_strs(district_polyline_strs,
                                                       district_name,
                                                       ax)
    plt.xticks([])
    plt.yticks([])  
    plt.axis('off')  
    
    
    # plt.savefig("E:\\xcsliu_project\\pycharm_obj\\city_district_polylines\\city_district_pic\\{}.jpg".format(city_name))  
    # plt.close(0) 
 




#'''

city_name = '北京市'
city_df = get_city_dataframe_by_city_name(city_name)




draw_pic_by_city_name(city_name)
    
'''   
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
                     
    city_list = c_list[:338]
    return city_list 
        
city_list = get_city_name_list()    
saved = []    

enmpty_file_city_list = ['儋州市','东莞市','嘉峪关市','中山市'] 
for idx, city in enumerate(city_list):
    if city not in saved and city not in enmpty_file_city_list:
        print (idx, city)
        draw_pic_by_city_name(city)
        saved.append(city)

#'''

