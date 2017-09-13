import sys
sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')

from constant import COMPLETE_DATA_HEADER_LIST, ANJUKE_SECOND_HAND_COMMUNITY_NAME_LIST, \
    ANJUKE_NEW_COMMUNITY_NAME_LIST, ANJUKE_UPDATE_HEADER_LIST
from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from dao.anjuke_dao import format_anjuke_new_community_raw_data, format_anjuke_second_hand_community_raw_data
from util import get_ready_data_file_path




# =====================
import numpy as np
import pandas as pd




def get_anjuke_community_raw_data(city_name):
    anjuke_new = format_anjuke_new_community_raw_data(city_name)
    anjuke_old = format_anjuke_second_hand_community_raw_data(city_name)
    return anjuke_old, anjuke_new


def consolidate_form(second_hand_community_data, new_community_data):
    # rename and drop
    second_hand_community_data.rename(columns={'truncate_name': 'name',
                                               'address': 'address',
                                               'mid_price': 'present_price'}, inplace=True)
    second_hand_community_data_with_drop = second_hand_community_data.drop(['id','mid_change'],axis = 1)

    new_community_data.rename(columns={'loupan_name': 'name',
                                       'address': 'address',
                                       'prop_num': 'prop_num',
                                       'baidu_lat': 'lat',
                                       'baidu_lng': 'lng',
                                       'new_price': 'start_price',
                                       'region_title': 'region',
                                       'sub_region_title': 'sub_region',
                                       'house_types': 'house_type',
                                       'kaipan_new_date': 'start_date'}, inplace=True)
    new_community_data_with_drop = new_community_data.drop(['loupan_id','metro_info'],axis = 1)
    
    # compliment old community
    old_header_to_add = [k for k in COMPLETE_DATA_HEADER_LIST if k not in ANJUKE_SECOND_HAND_COMMUNITY_NAME_LIST]
    column_num = len(old_header_to_add)
    row_num = len(second_hand_community_data)
    to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=old_header_to_add)
    consolidated_old = pd.concat([second_hand_community_data_with_drop, to_be_appended], axis=1)

    # compliment new community
    new_header_to_add = [k for k in COMPLETE_DATA_HEADER_LIST if k not in ANJUKE_NEW_COMMUNITY_NAME_LIST]
    column_num = len(new_header_to_add)
    row_num = len(new_community_data)
    to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=new_header_to_add)
    consolidated_new = pd.concat([new_community_data_with_drop, to_be_appended], axis=1)
    return consolidated_old, consolidated_new


def merge_community_raw_data(second_hand_community_data, new_community_data):
    # 把两个数据集重叠的部分整合在一起
    added_new_community_name_list = []
    # 遍历二手房
    for i in range(len(second_hand_community_data)):
        print(str(i) + '/' + str(len(second_hand_community_data)))
        row = second_hand_community_data.iloc[i]
        name = row['name']
        # 如果二手房的小区名称在新房中出现
        if not new_community_data[new_community_data['name'] == name].empty:
            added_new_community_name_list.append(name)
            idx = new_community_data[new_community_data['name'] == name].index[0]
            for header in ['present_price', 'prop_num']:
                new_community_data[header][idx] = second_hand_community_data.at[i, header]
    # 把重叠的部分从二手房数据集中去除
    for name in added_new_community_name_list:
        idx = second_hand_community_data[new_community_data['name'] == name].index[0]
        second_hand_community_data = second_hand_community_data.drop(idx)
    # 把两部分数据集拼合在一起
    total = pd.concat([new_community_data, second_hand_community_data], axis=0)
    total = total.reset_index(drop=True)
    return total
















city_name = '重庆'
anjuke_old, anjuke_new = get_anjuke_community_raw_data(city_name)
formed_anjuke_old, formed_anjuke_new = consolidate_form(anjuke_old, anjuke_new)

total = merge_community_raw_data(formed_anjuke_old, formed_anjuke_new)



formed_anjuke_old['address'].loc[5]




second_hand_community_data = formed_anjuke_old
new_community_data = formed_anjuke_new
added_new_community_name_list = []
# 遍历二手房
for i,row in second_hand_community_data.iterrows():
    print(str(i) + '/' + str(len(second_hand_community_data)))
    name = row['name']
    # 如果二手房的小区名称在新房中出现
    if not new_community_data[new_community_data['name'] == name].empty:
        added_new_community_name_list.append(name)
        idx = new_community_data[new_community_data['name'] == name].index[0]
        for header in ['present_price', 'prop_num']:
            new_community_data[header][idx] = second_hand_community_data.at[i,header]


idx = new_community_data[new_community_data['name'] == '皓宏阳光水岸'].index
print (idx)

merged_raw_data = merge_community_raw_data(formed_anjuke_old, formed_anjuke_new)

header = 'present_price'
new_community_data[header][0] = second_hand_community_data.at[36, header]

formed_anjuke_new.at[1,'address']

formed_anjuke_new.at[1,1]











anjuke_new.at[1,'address']
formed_anjuke_new.at[1,'address']

'''
city_name = '重庆'
ready_data_file_path = get_ready_data_file_path(city_name,
                                                CrawlerDataType.READY_DATA.value,
                                                CrawlerSourceName.ANJUKE.value,
                                                CrawlerDataLabel.SECOND_HAND_COMMUNITY.value)

E:\\PycharmPrjects\\poi\\poi\\poi_data\\chongqing\\raw_data\\2017_09_13


'''

c = anjuke_old[anjuke_old['truncate_name'] == '西郊庄园'].index
print (c)
