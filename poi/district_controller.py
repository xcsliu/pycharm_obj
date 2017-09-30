import pandas as pd
import json
from pypinyin import lazy_pinyin
from shapely.geometry import Polygon, Point, MultiPolygon
import matplotlib.pyplot as plt
from operator import itemgetter

from location_transfer import bd09_to_gcj02
from util import coordinate_distance


class DistrictController:
    
    def __init__(self, lng, lat):
        self.file_path_pattern = 'E:\\xcsliu_project\\pycharm_obj\\city_district_polylines\\{}.tsv'

        self.read_file_path = self.file_path_pattern.format('all_city_districts')
        self.pd_all_districts = pd.read_table(self.read_file_path, error_bad_lines=False, encoding = 'gbk')
        self.base_coordinate = bd09_to_gcj02(lng, lat)
        self.lng = self.base_coordinate[0]
        self.lat = self.base_coordinate[1]
        self.base_point = Point(self.lng, self.lat)
        self.city_name, self.district_name = self.get_city_and_district_by_coordinate(self.lng, self.lat)

    def get_city_and_district_by_coordinate(self, lng, lat):
        distance_list = []
        for idx, row in self.pd_all_districts.iterrows():
            district_center = row['district_center']
            coordinate = district_center.split(',')
            center_lng, center_lat = float(coordinate[0]), float(coordinate[1])
            distance = coordinate_distance(self.lng, self.lat, center_lng, center_lat)
            distance_list.append([idx, distance])
    
        sorted_distance_list =  sorted(distance_list, key=itemgetter(1))   
        for idx, distance in sorted_distance_list:
            district_polyline = json.loads( self.pd_all_districts.iloc[idx]['district_polyline'] )
            polygons_list = []
            for sub_district in district_polyline:
                polygon = Polygon(sub_district)
                polygons_list.append(polygon)
                
            polygons = MultiPolygon(polygons_list)
            if polygons.contains(self.base_point):
                city_name = self.pd_all_districts.iloc[idx]['city_name']
                district_name = self.pd_all_districts.iloc[idx]['district_name']
                break
        return city_name, district_name

    def plot_single_district_by_district_polyline_strs(self, district_polyline_strs, district_name, district_center, ax):
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
            if district_name == self.district_name:
               plt.fill(sub_district[0], sub_district[1], 'r', alpha=0.2)   
            else:
                plt.fill(sub_district[0], sub_district[1], 'g', alpha=0.5)    
            plt.plot(sub_district[0], sub_district[1], 'w-',linewidth=2)
    
        # 画出基地位置点
        plt.scatter(self.lng, self.lat,
                    s = 350, 
                    c = 'darkorange', 
                    marker = '*', 
                    alpha=0.9,
                    edgecolors = 'w')        
    
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
                    fontsize=14)    
        return center_point

    def draw_pic_by_city_name(self):
        city_df = self.pd_all_districts[self.pd_all_districts['city_name'] == self.city_name]
        
        # 画布初始化
        plt.rcParams['font.sans-serif']=['SimHei']
        fig = plt.figure(0)
        fig.set_size_inches(12, 12)
        ax = fig.add_subplot(111)

        # 所在城市各个行政区轮廓填充
        for idx, row in city_df.iterrows():
            district_name = row['district_name']
            district_polyline_strs = row['district_polyline']
            district_center = row['district_center']
            center_point = self.plot_single_district_by_district_polyline_strs(district_polyline_strs,
                                                                               district_name,
                                                                               district_center,
                                                                               ax)
        plt.xticks([])
        plt.yticks([])  
        plt.axis('off')  

        plt.savefig("E:\\xcsliu_project\\pycharm_obj\\city_district_polylines\\{}.jpg".format(self.city_name))
        plt.close(0)