import sys
sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')

from dao.anjuke_dao import format_anjuke_new_community_raw_data, format_anjuke_second_hand_community_raw_data
from dao.baidu_dao import format_baidu_poi_raw_data
from dao.fangtianxia_dao import format_fangtianxia_parcel_raw_data
from dao.lianjia_dao import format_lianjia_new_community_raw_data, format_lianjia_second_hand_community_raw_data


def get_anjuke_community_raw_data(city_name):
    anjuke_new = format_anjuke_new_community_raw_data(city_name)
    anjuke_old = format_anjuke_second_hand_community_raw_data(city_name)
    return anjuke_old, anjuke_new


def get_lianjia_community_raw_data(city_name):
    lianjia_new = format_lianjia_new_community_raw_data(city_name)
    lianjia_old = format_lianjia_second_hand_community_raw_data(city_name)
    return lianjia_old, lianjia_new


def get_baidu_raw_data(city_name):
    baidu_raw_data = format_baidu_poi_raw_data(city_name)
    return baidu_raw_data


def get_fangtianxia_raw_data(city_name):
    fangtianxia_raw_data = format_fangtianxia_parcel_raw_data(city_name)
    return fangtianxia_raw_data





city_name = '重庆'
anjuke_old, anjuke_new = get_anjuke_community_raw_data(city_name)

lianjia_old, lianjia_new = get_lianjia_community_raw_data(city_name)

baidu_raw_data = get_baidu_raw_data(city_name)

fangtianxia_raw_data = get_fangtianxia_raw_data(city_name)

