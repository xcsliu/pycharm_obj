# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 14:00:13 2017

@author: xcsliu


绘图

有的行政区虽然名义上是一个，但是从形状上被分成了2个
"""

import pandas as pd
import json
from pypinyin import lazy_pinyin
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt



def form_str_to_json(strs):
    json_strs = strs.replace('|','],[')
    return json_strs

city_name = '沧州市'
city_name_pinyin = ''.join(lazy_pinyin(city_name))
file_path_pattern = 'E:\\xcsliu_project\\pycharm_obj\\city_district_polylines\\{}.tsv'
file_path = file_path_pattern.format(city_name_pinyin)

districts_pd = pd.read_table(file_path, error_bad_lines=False, encoding='gbk')

districts_series = districts_pd['district_polyline']

# 处理 city 的 x 和 y


# city_polygon_list = json.loads(to_json)
'''
for k in city_polygon_list:
    tmp_x.append(k[0])
    tmp_y.append(k[1])
city_to_plot.append(tmp_x)
city_to_plot.append(tmp_y)
'''
# 处理 district 的 x 和 y
'''
districts_in = []

for idx,i in enumerate(districts_series):
    i = form_str_to_json(i)
    print (idx)
    district_polygon = json.loads(i)
    tmp_x, tmp_y = [], []
    for k in district_polygon:
        tmp_x.append(k[0])
        tmp_y.append(k[1])
    districts_in.append([tmp_x, tmp_y])


plt.rcParams['font.sans-serif']=['SimHei']
fig = plt.figure(0)
fig.set_size_inches(10, 10)
ax = fig.add_subplot(111)

for idx, district in enumerate(districts_in[0:6]):
    plt.plot(district[0], district[1], 'w-',linewidth=1)
    plt.fill(district[0], district[1], 'r', alpha=0.3)
    
    strs_to_json = form_str_to_json(districts_series[idx])
    district = json.loads(strs_to_json)
    polygon_obj = Polygon(district)
    center_point = [list(polygon_obj.centroid.coords)[0][0], 
                    list(polygon_obj.centroid.coords)[0][1]]
    
    ax.annotate(districts_pd.loc[idx,u'district_name'],   
                xy = (center_point[0], center_point[1]), 
                xycoords='data',
                fontsize=10)  
'''    
# =====
plt.rcParams['font.sans-serif']=['SimHei']
fig = plt.figure(0)
fig.set_size_inches(12, 12)
ax = fig.add_subplot(111)

district_polyline_strs = districts_series[6]
district_name = '曹妃甸区'


district_polyline_strs_to_json = district_polyline_strs.replace('|',']]|[[')
sub_district_polyline_strs_list = district_polyline_strs_to_json.split('|')

# 所有待画图的区块
sub_districts_in = []
for idx, i in enumerate(sub_district_polyline_strs_list):
    district_polygon = json.loads(i)
    tmp_x, tmp_y = [], []
    for k in district_polygon:
        tmp_x.append(k[0])
        tmp_y.append(k[1])
    sub_districts_in.append([tmp_x, tmp_y])

# 画出轮廓并且填充颜色
for idx, sub_district in enumerate( sub_districts_in ):
    plt.fill(sub_district[0], sub_district[1], 'r', alpha=0.3)            


# 计算中心点位置：
center_point_x_list = []
center_point_y_list = []
for idx, i in enumerate(sub_district_polyline_strs_list):
    district_polygon = json.loads(i)
    polygon_obj = Polygon(district_polygon)
    center_point_x_list.append(list(polygon_obj.centroid.coords)[0][0])
    center_point_y_list.append(list(polygon_obj.centroid.coords)[0][1])
center_x = float( sum(center_point_x_list) / len(center_point_x_list) )
center_y = float( sum(center_point_y_list) / len(center_point_y_list) )
center_point = [center_x, center_y]
      

# 标注行政区名称
ax.annotate(district_name,   
        xy = (center_point[0], center_point[1]), 
        xycoords='data',
        fontsize=12) 
# =====    
    
    
plt.xticks([])
plt.yticks([])  
plt.axis('off')  
# =============









# =============

plt.savefig("E:\\xcsliu_project\\pycharm_obj\\city_district_polylines\\city_district_pic\\{}.jpg".format(city_name))  
plt.close(0) 





'''
# plt.fill(district[0], district[1], 'g', alpha=0.3, linewidth=2 )    
# plt.plot(city_to_plot[0], city_to_plot[1], 'b--',linewidth=1)    
    
plt.savefig("E:\\xcsliu_project\\pycharm_obj\\city_district_polylines\\city_district_pic\\{}.jpg".format(city_name))  
plt.close(0)     

#from pylab import *  
# mpl.rcParams['font.sans-serif'] = ['SimHei']  

    
    
  


district = json.loads(districts_series[1])
polygon_obj = Polygon(district)
center_point = [list(polygon_obj.centroid.coords)[0][0], 
                list(polygon_obj.centroid.coords)[0][1]]

ax.annotate(num_text[11],
            xy = (center_point[0], center_point[1]), 
            xycoords='data',
            fontsize=20)  

    # fig.fill(district[0], district[1] , 'b' , alpha=0.3)
    

ax.annotate('①',
            xy = (113.5034356, 23.46123), 
            xycoords='data',
            fontsize=20) 

    polygon_obj = Polygon(district)
    center_point = [list(polygon_obj.centroid.coords)[0][0], 
                    list(polygon_obj.centroid.coords)[0][1]]
    ax.annotate(num_text[idx],
                xy = (center_point[0], center_point[1]), 
                xycoords='data',
                fontsize=20) 


plt.show()

num_text = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'


print (num_text[11])




import numpy as np

def f(t):
    return np.exp(-t) * np.cos(2 * np.pi * t)
t1 = np.arange(0, 5, 0.1)
t2 = np.arange(0, 5, 0.02)

plt.figure(12)
plt.subplot(421)
plt.plot(t1, f(t1), 'bo', t2, f(t2), 'r--')

plt.subplot(422)
plt.plot(t2, np.cos(2 * np.pi * t2), 'r--')

plt.subplot(4,1,2)
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])

plt.show()

'''










    
    