import numpy as np
from dao.anjuke_dao import process_anjuke_new_community_raw_data, process_anjuke_second_hand_community_raw_data
import pandas as pd

city_name = '重庆'
name_list_to_add_into_new_community_data = ['community_id',
                                            'community_address',
                                            'community_mid_price',
                                            'community_mid_change',
                                            'community_lat',
                                            'community_lng',
                                            'community_prop_num']

name_list_to_add_into_old_community_data = ['loupan_address',
                                            'loupan_lat',
                                            'loupan_lng',
                                            'loupan_prop_num',
                                            'loupan_id',
                                            'loupan_price',
                                            'metro_info',
                                            'build_type',
                                            'developer',
                                            'fitment_type',
                                            'house_types',
                                            'kaipan_new_date',
                                            'region_title',
                                            'sub_region_title']


def get_anjuke_community_raw_data(city_name):
    anjuke_new = process_anjuke_new_community_raw_data(city_name)
    anjuke_old = process_anjuke_second_hand_community_raw_data(city_name)
    return anjuke_old, anjuke_new


def consolidate_form(second_hand_community_data, new_community_data):
    # rename
    second_hand_community_data.rename(columns={'truncate_name': 'community_name',
                                               'address': 'community_address',
                                               'id': 'community_id',
                                               'mid_price': 'community_mid_price',
                                               'prop_num': 'community_prop_num',
                                               'lat': 'community_lat',
                                               'lng': 'community_lng',
                                               'mid_change': 'community_mid_change'}, inplace=True)

    new_community_data.rename(columns={'loupan_name': 'community_name',
                                       'address': 'loupan_address',
                                       'prop_num': 'loupan_prop_num',
                                       'baidu_lat': 'loupan_lat',
                                       'baidu_lng': 'loupan_lng',
                                       'new_price': 'loupan_price'}, inplace=True)
    # drop_duplicate
    second_hand_community_data = second_hand_community_data.drop_duplicates(['community_name'])
    second_hand_community_data = second_hand_community_data.reset_index(drop=True)
    new_community_data = new_community_data.drop_duplicates(['community_name'])
    new_community_data = new_community_data.reset_index(drop=True)

    # compliment old community
    column_num = len(name_list_to_add_into_old_community_data)
    row_num = len(second_hand_community_data)
    to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=name_list_to_add_into_old_community_data)
    dframe_old = pd.concat([second_hand_community_data, to_be_appended], axis=1)

    for column_name in name_list_to_add_into_old_community_data:
        second_hand_community_data[column_name] = None

    # compliment new community
    column_num = len(name_list_to_add_into_new_community_data)
    row_num = len(new_community_data)
    to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=name_list_to_add_into_new_community_data)
    dframe_new = pd.concat([new_community_data, to_be_appended], axis=1)

    for column_name in name_list_to_add_into_new_community_data:
        new_community_data[column_name] = None
    return dframe_old, dframe_new


def merge_community_data(second_hand_community_data, new_community_data):
    old_community = second_hand_community_data.copy()
    new_community = new_community_data.copy()
    # 把两个数据集重叠的部分小区信息整合在一起
    added_new_community_name_list = []
    for i in range(len(old_community)):
        print(str(i) + '/' + str(len(old_community)))
        row = old_community.iloc[i]
        name = row['community_name']
        if not new_community[new_community['community_name'] == name].empty:
            added_new_community_name_list.append(name)
            idx = new_community[new_community['community_name'] == name].index[0]
            for new_name in name_list_to_add_into_old_community_data:
                old_community[new_name][i] = new_community.at[idx, new_name]
    #
    for name in added_new_community_name_list:
        idx = new_community[new_community['community_name'] == name].index[0]
        new_community = new_community.drop(idx)

    total = pd.concat([new_community, old_community], axis=0)
    total = total.reset_index(drop=True)
    return total

def get_anjuke_ready_data():
    ready_data_file_path = ''
    ready_data = pd.read_table(ready_data_file_path, error_bad_lines=False)
    return ready_data

