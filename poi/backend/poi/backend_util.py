import os

from pypinyin import lazy_pinyin
from math import radians, cos, sin, asin, sqrt


def get_data_file_path(city_name, date):
    city_name_pinyin = ''.join(lazy_pinyin(city_name))
    data_type = 'ready_data'
    source_name = 'insensitive_source'
    data_label = 'total_data'
    path = os.path.join(os.path.dirname(os.getcwd()), 'poi_data', city_name_pinyin, data_type, str(date))
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = '{}_{}_{}_{}.tsv'.format(city_name_pinyin, source_name, data_label, date)
    file_path = os.path.join(path, file_name)
    return file_path


def convert_km_to_lat_lng(lat, lng, width_in_km):
    ratio_lat = coordinate_distance(lng, lat, lng, lat+1)
    ratio_lng = coordinate_distance(lng, lat, lng+1, lat)

    dif_lat = width_in_km / ratio_lat / 2
    dif_lng = width_in_km / ratio_lng / 2

    return dif_lat, dif_lng


def coordinate_distance(lng1, lat1, lng2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    # 将十进制度数转化为弧度
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine公式
    d_lng = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lng / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r