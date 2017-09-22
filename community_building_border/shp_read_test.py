# -*- coding: utf-8 -*-
"""
plot border based on shp file 

https://github.com/smft/draw_basemap_from_shp_file

重庆：
106.53063501341296 29.54460610888615


106.030635 29.044606
107.030635 30.044606

北京：
116.39564503787867 39.92998577808024
上海：
121.48789948569473 31.24916171001514
广州：
113.30764967515182 23.12004910207623
深圳：
114.0259736573215 22.546053546205247
天津：
117.21081309155257 39.143929903310074



尝试一下分成 5X5的情况，是否可以全集下载

"""
import time
import shapefile
import pandas as pd
# from matplotlib import pyplot as plt
def get_date(format="%Y_%m_%d"):
    date = time.strftime(format, time.localtime())
    return date


# border_shape=shapefile.Reader("/media/qzhang/240E5CF90E5CC608/dunoinfo/province/bou2_4p.shp")
border_shape=shapefile.Reader('E:\\水经注data\\tianjin\\tianjin3\\未命名(7)_面部分.shp')
record = border_shape.iterRecords()
border=border_shape.shapes()

# ==================
# 画图，提取polygon
polygon_list = []
count=0
for border_detail in border:
    print (count) 
    border_points=border_detail.points
    polygon_list.append(border_points)
    #fig=plt.subplots()
    #x,y = [],[]
    #for cell in border_points:
    #    x.append(cell[0])
    #    y.append(cell[1])
    #    plt.plot(x,y,'b-', linewidth=2)
    #plt.show()
    count+=1
# 16046
# ==================
# 提取 floor 
floor_list = []
record = border_shape.iterRecords()
for idx,floor_data in enumerate(record):
    print (floor_data)
    floor_list.append(int(floor_data[1]))
# ==================
# 整合对应关系
data_list = []
for i in range( len(polygon_list) ):
    data_list.append([floor_list[i],polygon_list[i]])


data_list_3 = data_list


# ===================
data_list = data_list_1 + data_list_2 + data_list_3 # + data_list_4 + data_list_5

date = get_date()

city_name = 'tianjin'

save_file_path = 'E:\\building_processed_data\\{}_building_border_{}.tsv'.format(city_name, date)

points_list_pd = pd.DataFrame(data_list)

points_list_pd.to_csv(path_or_buf=save_file_path, sep='\t', encoding='utf-8')

