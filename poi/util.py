import platform
import time
import os
import pandas as pd
from pypinyin import lazy_pinyin

from constant import CITY_LIST


def save_raw_data_in_tsv_file(file_path, data_dict_list):
    data_dict_list_pd = pd.DataFrame(data_dict_list)
    data_dict_list_pd.to_csv(path_or_buf=file_path, sep='\t', encoding='utf-8')


def get_date(format="%Y_%m_%d"):
    date = time.strftime(format, time.localtime())
    return date


def is_windows_system():
    return 'Windows' in platform.system()


def get_raw_data_file_path(city_name, data_type, source_name, data_label):
    date = get_date()
    city_name_pinyin = ''.join(lazy_pinyin(city_name))
    # raw data path  : poi/poi_data/city/raw_data  /date/1.anjuke_old 2.anjuke_new 3.lianjia_old 4.lianjia_new 5.baidu 6.fangtianxia
    # ready_data path: poi/poi_data/city/ready_data/1.anjuke 2.lianjia 3.baidu 4.fangtianxia
    path = os.path.join(os.path.dirname(os.getcwd()), 'poi', 'poi_data', city_name_pinyin, data_type, str(date))
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = path + '\{}_{}_{}_{}.tsv'.format(city_name_pinyin, source_name, data_label, date)
    if not is_windows_system():
        linux_file_path = file_path.replace('\\', '/')
        return linux_file_path
    return file_path

def get_ready_data_file_path(city_name, data_type, source_name, data_label):
    city_name_pinyin = ''.join(lazy_pinyin(city_name))
    # raw data path  : poi/poi_data/city/raw_data  /date/1.anjuke_old 2.anjuke_new 3.lianjia_old 4.lianjia_new 5.baidu 6.fangtianxia
    # ready_data path: poi/poi_data/city/ready_data/1.anjuke 2.lianjia 3.baidu 4.fangtianxia
    path = os.path.join(os.path.dirname(os.getcwd()), 'poi', 'poi_data', city_name_pinyin, data_type)
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = path + '\{}_{}_{}.tsv'.format(city_name_pinyin, source_name, data_label)
    if not is_windows_system():
        linux_file_path = file_path.replace('\\', '/')
        return linux_file_path
    return file_path



def get_city_name_by_day():
    day = time.strftime("%j", time.localtime())
    num = int(day) % len(CITY_LIST)
    return CITY_LIST[num]