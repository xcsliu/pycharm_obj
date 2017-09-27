# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 10:36:08 2017

@author: xcsliu
guangyang:
    
from shapely.geometry import Polygon, Point

polygon.contains(Point(point))


小区和建筑轮廓合并
通过一个城市做一个示范，看看合成效果
"""
from shapely.geos import TopologicalError
from shapely.geometry import Polygon, Point
import pandas as pd
import json
import time
import matplotlib.pyplot as plt
'''
p = Polygon([[0,0], [0,2], [2,2],[2,0]])
p.boundary
p.centroid
print(list(p.centroid.coords))
'''

city_name = 'shanghai'

def get_building_and_community_border_with_city_name(city_name):
    building_border_path = 'E:\\building_processed_data\\{}_building_border_2017_09_07.tsv'.format(city_name)
    community_border_path = 'E:\\building_processed_data\\{}_community_border_with_wgs84_2017_09_06.tsv'.format(city_name)
    building_border = pd.read_table(building_border_path)
    community_border = pd.read_table(community_border_path)
    return building_border, community_border

def get_date(format="%Y_%m_%d"):
    date = time.strftime(format, time.localtime())
    return date

# 输入为 community_border 的 index，输出为该 community 对应的 polygon 对象和 community name
def get_community_border_and_name(community_border, idx):
    c_border = community_border.ix[idx,4]
    c_name = community_border.ix[idx,2]
    c_list = json.loads(c_border)
    return c_list, c_name

# 将小区轮廓的坐标 list 转换为 polygon object
def get_community_polygon_object(border_list):
    tmp = []
    for i in border_list:
        tmp.append([i[0],i[1]])
    tmp_polygon = Polygon(tmp)    
    return tmp_polygon


def process_building_border(building_border):
    tmp_list = []
    tmp_lat_list = []
    tmp_lng_list = []
    for index,row in building_border.iterrows():
        p_border = row[2]
        test_str_processed = p_border.replace('(','[').replace(')',']')
        p_list = json.loads(test_str_processed)
        tmp_list.append(p_list)
        tmp_lat_list.append(p_list[0][1])
        tmp_lng_list.append(p_list[0][0])
    building_border['point_list'] = tmp_list
    building_border['point_lat'] = tmp_lat_list
    building_border['point_lng'] = tmp_lng_list

# 检测各个建筑是否在该小区内
def get_useful_building_list(community_border_list, building_border):
    # community_border_list 转换为 polygon 的对象
    tmp = []
    for i in community_border_list:
        tmp.append([i[0],i[1]])
    community_polygon_obj = Polygon(tmp)    
    # =============
    center_lng = list(community_polygon_obj.centroid.coords)[0][0]
    center_lat = list(community_polygon_obj.centroid.coords)[0][1]
    tmp_building_border = building_border[(building_border['point_lat']<center_lat+0.02)&
                                          (building_border['point_lat']>center_lat-0.02)&
                                          (building_border['point_lng']<center_lng+0.02)&
                                          (building_border['point_lng']>center_lng-0.02)]
    # =============
    useful_building_list = []
    # len_buildings = len(tmp_building_border)
    num = 0
    building_coverage_area = 0
    building_plot_area = 0
    for index,row in tmp_building_border.iterrows():
        num += 1
        # print (str(num)+'/'+str(len_buildings))
        p_list = row[3] 
        p_floor = row[1]
        building_polygon_obj = Polygon(p_list)
        point_lng = list(building_polygon_obj.centroid.coords)[0][0]
        point_lat = list(building_polygon_obj.centroid.coords)[0][1]
        p_point = Point([point_lng,point_lat])
        # 建筑物中心点落在小区内，同时建筑物在小区内的面积占建筑物面积的百分之五十以上的，记录下来
        try:
            if community_polygon_obj.contains(p_point) and community_polygon_obj.intersection(building_polygon_obj).area / building_polygon_obj.area > 0.5:
                useful_building_list.append([p_floor,p_list])
                building_coverage_area += building_polygon_obj.area
                building_plot_area += building_polygon_obj.area * p_floor
        except TopologicalError:
            pass

        
    # 小区建筑覆盖率低于 0.05 的直接排除
    # plot ratio
    # coverage ratio
    coverage_ratio = building_coverage_area / community_polygon_obj.area
    plot_ratio = building_plot_area / community_polygon_obj.area
    if coverage_ratio < 0.1 or len(useful_building_list) < 2:
        useful_building_list = []
    elif plot_ratio < 1:
        if len(useful_building_list) < 20:
            useful_building_list = []
    return coverage_ratio, plot_ratio, useful_building_list


# 68.54 s



def get_useful_community_list(community_border, index_in_list):
    total_info = []
    num = 0
    total_len = len(community_border)
    for index,row in community_border.iterrows():
        num += 1
        print (str(index_in_list) + ' - ' + str(num) + '/' + str(total_len))
        tmp = []
        c_list, community_name = get_community_border_and_name(community_border, index)
        coverage_ratio, plot_ratio, building_in_community = get_useful_building_list(c_list, building_border)
        tmp.append(community_name)         #  小区名字
        tmp.append(c_list)                 #  小区轮廓
        tmp.append(building_in_community)  #  小区建筑
        tmp.append(coverage_ratio)         #  建筑覆盖率
        tmp.append(plot_ratio)             #  容积率
        if tmp[2] != []:
            total_info.append(tmp)
    return total_info
    # ====================
    # 数据存储

    


# 得到当前城市的建筑边界和小区边界
building_border, community_border = get_building_and_community_border_with_city_name(city_name)
process_building_border(building_border)
# 
# community_border = community_border[2600:2610]
community_border = community_border[2768:]
step_num = 300
num = (int(len(community_border)/step_num))
if [community_border[step_num*num:]] != []:
    community_border_list = [community_border[i*(step_num):(i+1)*step_num] for i in range(num)] + [community_border[step_num*num:]]
else:
    community_border_list = [community_border[i*(step_num):(i+1)*step_num] for i in range(num)]

start = time.clock()
num_of_useful_community = 0
for idx,tmp_community_border in enumerate(community_border_list):
    tmp_total_info = get_useful_community_list(tmp_community_border, idx)
    
    #

    date = get_date()
    save_file_path = 'E:\\x-kool-home\\community_and_building_border\\{}_ready_community_{}_{}.tsv'.format(city_name, date, idx)
    points_list_pd = pd.DataFrame(tmp_total_info)
    points_list_pd.to_csv(path_or_buf=save_file_path, sep='\t', encoding='utf-8',index=False)    

    
    l_total = len(tmp_total_info)
    for num in range(l_total):
        c_list = tmp_total_info[num][1]
        building_in_community = tmp_total_info[num][2]
        print (tmp_total_info[num][0],tmp_total_info[num][3],tmp_total_info[num][4],len(tmp_total_info[num][2]))
        # ========== plot ============================
        # 处理 community 的 x 和 y
        community_to_plot = []
        tmp_x, tmp_y = [], []
        for k in c_list:
            tmp_x.append(k[0])
            tmp_y.append(k[1])
        community_to_plot.append(tmp_x)
        community_to_plot.append(tmp_y)
        # 处理 building 的 x 和 y
        builds_in = []
        for i in building_in_community:
            tmp_x, tmp_y = [], []
            for k in i[1]:
                tmp_x.append(k[0])
                tmp_y.append(k[1])
            builds_in.append([tmp_x, tmp_y])
        
        # [poly1, poly2]
        # gpd.GeoSeries(p[]).plot()
        # plt.plot(community_to_plot[0], community_to_plot[1], marker='o')
        fig = plt.figure(0)
        plt.plot(community_to_plot[0], community_to_plot[1], 'b-',linewidth=2)
        for building in builds_in:
            plt.plot(building[0], building[1], 'r-',linewidth=2)
        # plt.show()
        community_name = tmp_total_info[num][0]
        community_name = community_name.replace('/','·')
        plt.savefig("{}_{}_{}_{:.3f}_{:.3f}_{}.jpg".format(city_name, num+num_of_useful_community, community_name, tmp_total_info[num][3], tmp_total_info[num][4], len(tmp_total_info[num][2])))  
        plt.close(0)    
    num_of_useful_community += len(tmp_total_info)

end = time.clock()
print('运行时间：%-.2f s' % (end - start))


fig = plt.figure(0)
ax = fig.add_subplot(111)
# ====================

'''
num_of_file = 11
for idx in range(num_of_file):
    city_name = ''
    date = get_date()
    read_file_path = 'E:\\x-kool-home\\community_and_building_border\\{}_ready_community_{}_{}.tsv'.format(city_name, date, idx)
    ready_data.to_csv(path_or_buf=read_file_path, sep='\t', encoding='utf-8')
    



a = Polygon([[0,0],[2,0],[2,0],[0,0]])
b = Polygon([[0,0],[1,0],[1,1],[0,1]])

c = Polygon([[3,3],[3,4],[4,4],[4,3]])


a.intersection(c).area / a.area


'''
# ====================
'''
c_list = json.loads( community_border.at[1959,'wgs84'] ) 

community_to_plot = []
tmp_x, tmp_y = [], []
for k in c_list:
    tmp_x.append(k[0])
    tmp_y.append(k[1])
community_to_plot.append(tmp_x)
community_to_plot.append(tmp_y)
fig = plt.figure(0)
plt.plot(community_to_plot[0], community_to_plot[1], 'b-',linewidth=2)
plt.show()


idx = 0
city_name = 'shanghai'
date = get_date()
read_file_path = 'E:\\x-kool-home\\community_and_building_border\\{}_ready_community_{}_{}.tsv'.format(city_name, date, idx)
raw_data = pd.read_table(read_file_path, error_bad_lines=False)


community_obj = Polygon(c_list)
build_list = json.loads(raw_data.at[20,'2'])
for idx,i in enumerate(build_list):
    ply_obj = Polygon(i[1])
    print (idx)
    if community_obj.intersection(ply_obj).area / ply_obj.area > 0.5:
        print (ply_obj.area)

build_list[39]

test_obj = Polygon(build_list[39][1])
if community_obj.intersection(test_obj):
    print (1)
else:
    print (2)
test_obj.boundary
test_obj.area

a = '报春三/四村'
a = a.replace('/','·')
community_border[community_border['0'] == '宝地新品居']
'''





