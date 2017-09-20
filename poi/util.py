import platform
import time
import os
import pandas as pd
from pypinyin import lazy_pinyin
from math import radians, cos, sin, asin, sqrt

from constant import CITY_LIST


def save_raw_data_in_tsv_file(file_path, data_dict_list):
    data_dict_list_pd = pd.DataFrame(data_dict_list)
    data_dict_list_pd.to_csv(path_or_buf=file_path, sep='\t', encoding='utf-8')


def is_windows_system():
    return 'Windows' in platform.system()


def get_data_file_path(city_name, data_type, source_name, data_label, date):
    city_name_pinyin = ''.join(lazy_pinyin(city_name))
    path = os.path.join(os.path.dirname(os.getcwd()), 'poi_data', city_name_pinyin, data_type, str(date))
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = '{}_{}_{}_{}.tsv'.format(city_name_pinyin, source_name, data_label, date)
    file_path = os.path.join(path, file_name)
    return file_path


def get_city_name_by_day():
    day = time.strftime("%j", time.localtime())
    num = int(day) % len(CITY_LIST)
    return CITY_LIST[num]


def coordinate_distance(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r