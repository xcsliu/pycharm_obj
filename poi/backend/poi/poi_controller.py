import sys

sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')


import json
import numpy as np
import pandas as pd

from backend.poi.model.residence_model import Residence
from backend.poi.backend_util import convert_km_to_lat_lng, get_data_file_path

from xkool_date_util import XkDateUtil


def get_satellite_image_url():  # 卫星图
    return ''


def get_city_view_image_url():  # 城市景观图
    return ''


# 城市配套
def get_surrounding_poi_image_url():  # 城市配套图片
    return ''


def get_surrounding_summary_by_category():
    return {
        'traffic':   '',
        'hospital':  '',
        'education': '',
        'medical':   '',
        'landmark':  ''
    }


def get_street_summary():  # 周边街景描述文字
    return ''


def get_street_view_image_url_by_direction():
    return {
        'east':  '',
        'south': '',
        'west':  '',
        'north': '',
    }


def get_surrounding_residence_analysis(city_name, lng, lat, width_in_km):  # 周边户型分析, 数据结构? json?
    surrounding_communities_dataframe = get_surrounding_poi_dataframe(city_name, lng, lat, width_in_km)
    res_list = []
    for index, row in surrounding_communities_dataframe.iterrows():
        residence_type_list = json.loads(row['house_type'])
        for house_type in residence_type_list:
            
            unit_price = row['present_price'] if not np.isnan(row['present_price']) else row['start_price']
            residence_name = '{}户型'.format(str(int(float(house_type[1]))))
            community_name = row['name']
            residence_type = house_type[0]
            residence_area = int(float(house_type[1]))
            build_type = row['build_type']
            total_price = int(residence_area*int(float(unit_price)))
            
            residence_obj = Residence(residence_name,
                                      community_name,
                                      residence_type,
                                      residence_area,
                                      build_type,
                                      total_price)
            res_list.append(residence_obj)
    return res_list


def get_surrounding_community_analysis():  # 周边小区分析, 数据结构? json?

    return ''


def get_surrounding_traffic_value_image_url():  # 图片 或者 图片链接
    return ''


def get_surrounding_land_value_image_url():  # 图片 或者 图片链接
    return ''


def get_surrounding_poi_dataframe(city_name, lng, lat, width_in_km):
    xkool_date = XkDateUtil()
    golden_data_path = get_data_file_path(city_name, xkool_date.today_string)
    ready_data = pd.read_table(golden_data_path, error_bad_lines=False, encoding = 'gbk')
    dif_lat, dif_lng = convert_km_to_lat_lng(lat, lng, width_in_km)
    new_data = ready_data[(ready_data['lat'] > lat - dif_lat )&
                          (ready_data['lat'] < lat + dif_lat )&
                          (ready_data['lng'] > lng - dif_lng )&
                          (ready_data['lng'] < lng + dif_lng)]
    return new_data


def get_surrounding_community_dataframe(city_name, lng, lat, width_in_km):
    total_data = get_surrounding_poi_dataframe(city_name, lng, lat, width_in_km)
    data = total_data[total_data['data_poi'] == 'community']
    return data


def get_surrounding_baidu_poi_dataframe(city_name, lng, lat, width_in_km):
    total_data = get_surrounding_poi_dataframe(city_name, lng, lat, width_in_km)
    data = total_data[total_data['data_poi'] == 'baidu_poi']
    return data


def get_surrounding_land_dataframe(city_name, lng, lat, width_KM):
    total_data = get_surrounding_poi_dataframe(city_name, lng, lat, width_KM)
    data = total_data[total_data['data_poi'] == 'land']
    return data



city_name = '重庆'
lng = 106.480126
lat = 29.49608
width_in_km = 10

surrounding_communities_dataframe = get_surrounding_poi_dataframe(city_name, lng, lat, width_in_km)

res_list = get_surrounding_residence_analysis(city_name, lng, lat, width_in_km)

for i in res_list:
    print (i.residence_name, i.residence_type, i.residence_area, i.build_type, i.total_price)

'''
surrounding_communities_dataframe = get_surrounding_poi_dataframe(city_name, lng, lat, width_in_km)




row = surrounding_communities_dataframe.iloc[2]
residence_type_list = json.loads(row['house_type'])
for house_type in residence_type_list:
    
    unit_price = row['present_price'] if not np.isnan(row['present_price']) else row['start_price']
    residence_name = '{}户型'.format(str(int(float(house_type[1]))))
    community_name = row['name']
    residence_type = house_type[0]
    residence_area = int(float(house_type[1]))
    build_type = row['build_type']
    total_price = int(residence_area*int(float(unit_price)))
'''