import sys
sys.path.append('E:\\PycharmPrjects\\poi')



import pandas as pd
import numpy as np
from dao.lianjia_dao import format_lianjia_new_community_raw_data, format_lianjia_second_hand_community_raw_data


# =====================

name_list_to_add_into_new_community_data = ['community_id',
                                            'community_avg_unit_price',
                                            'community_bs_avg_unit_price',
                                            'community_min_price_total',
                                            'community_lat',
                                            'community_lng',
                                            'community_prop_num']

name_list_to_add_into_old_community_data = ['loupan_lat',
                                            'loupan_lng',
                                            'resblock_id',
                                            'loupan_avg_price',
                                            'build_type',
                                            'loupan_house_type',
                                            'loupan_frame_area',
                                            'loupan_min_frame_area',
                                            'loupan_max_frame_area']


def get_lianjia_community_raw_data(city_name):
    lianjia_new = format_lianjia_new_community_raw_data(city_name)
    lianjia_old = format_lianjia_second_hand_community_raw_data(city_name)
    return lianjia_old, lianjia_new


def consolidate_form(second_hand_community_data, new_community_data):
    # rename
    second_hand_community_data.rename(columns={'name': 'community_name',
                                               'id': 'community_id',
                                               'avg_unit_price': 'community_avg_unit_price',
                                               'bs_avg_unit_price': 'community_bs_avg_unit_price',
                                               'house_count': 'community_prop_num',
                                               'latitude': 'community_lat',
                                               'longitude': 'community_lng',
                                               'min_price_total': 'community_min_price_total'}, inplace=True)

    new_community_data.rename(columns={'resblock_name': 'community_name',
                                       'house_type': 'build_type',
                                       'latitude': 'loupan_lat',
                                       'longitude': 'loupan_lng',
                                       'average_price': 'loupan_avg_price',
                                       'rooms': 'loupan_house_type',
                                       'resblock_frame_area': 'loupan_frame_area',
                                       'min_frame_area': 'loupan_min_frame_area',
                                       'max_frame_area': 'loupan_max_frame_area'}, inplace=True)

    # compliment old community
    column_num = len(name_list_to_add_into_old_community_data)
    row_num = len(second_hand_community_data)
    to_be_appended = pd.DataFrame([[np.nan]*column_num]*row_num, columns=name_list_to_add_into_old_community_data)
    consolidated_old = pd.concat([second_hand_community_data, to_be_appended], axis=1)

    # compliment new community
    column_num = len(name_list_to_add_into_new_community_data)
    row_num = len(new_community_data)
    to_be_appended = pd.DataFrame([[np.nan]*column_num]*row_num, columns=name_list_to_add_into_new_community_data)
    consolidated_new = pd.concat([new_community_data, to_be_appended], axis=1)
    
    return consolidated_old, consolidated_new


def merge_community_data(second_hand_community_data, new_community_data):
    # 把两个数据集重叠的部分小区信息整合在一起
    added_old_community_name_list = []
    for i in range(len(new_community_data)):
        print (str(i)+'/'+str(len(new_community_data)))
        row = new_community_data.iloc[i]
        name = row['community_name']
        build_type = row['build_type']
        if not second_hand_community_data[second_hand_community_data['community_name'] == name].empty:
            if build_type == '住宅':
                added_old_community_name_list.append(name)
                idx = second_hand_community_data[second_hand_community_data['community_name'] == name].index[0]
                for new_name in name_list_to_add_into_new_community_data:
                    new_community_data[new_name][i] = second_hand_community_data.at[idx, new_name]
    
    
    num_note = 0
    for name in added_old_community_name_list:
        num_note += 1
        print (num_note)
        for idx in second_hand_community_data[second_hand_community_data['community_name'] == name].index:
            second_hand_community_data = second_hand_community_data.drop(idx)
        
    total = pd.concat([second_hand_community_data, new_community_data], axis=0)
    total = total.reset_index(drop=True)
    return total


def compliment_raw_data_into_ready_data(raw_data, ready_data):
    added_raw_data_name_list = []
    for k in range(len(raw_data)):
        row = ready_data.iloc[k]
        name = row['community_name']
        if not raw_data[raw_data['community_name'] == name].empty:
            added_raw_data_name_list.append(name)
            idx = raw_data[raw_data['community_name'] == name].index[0]
            for header in ANJUKE_UPDATE_HEADER_LIST:
                ready_data[header][k] = raw_data.at[idx, header]
            for house_type in raw_data.at[idx, 'houses_type']:
                if house_type not in ready_data['houses_type']:
                    ready_data['houses_type'].append(house_type)

    for name in added_raw_data_name_list:
        idx = raw_data[raw_data['community_name'] == name].index[0]
        raw_data = raw_data.drop(idx)

    total = pd.concat([raw_data, ready_data], axis=0)
    total = total.reset_index(drop=True)
    return total






# =========================================
city_name = '重庆'
lianjia_old, lianjia_new = get_lianjia_community_raw_data(city_name)
formed_lianjia_old, formed_lianjia_new = consolidate_form(lianjia_old, lianjia_new)


new_community_data = formed_lianjia_new
second_hand_community_data = formed_lianjia_old



added_old_community_name_list = []
for i in range(len(new_community_data)):
    print (str(i)+'/'+str(len(new_community_data)))
    row = new_community_data.iloc[i]
    name = row['community_name']
    build_type = row['build_type']
    if not second_hand_community_data[second_hand_community_data['community_name'] == name].empty:
        if build_type == '住宅':
            added_old_community_name_list.append(name)
            idx = second_hand_community_data[second_hand_community_data['community_name'] == name].index[0]
            for new_name in name_list_to_add_into_new_community_data:
                new_community_data[new_name][i] = second_hand_community_data.at[idx, new_name]


num_note = 0
for name in added_old_community_name_list:
    num_note += 1
    print (num_note)
    for idx in second_hand_community_data[second_hand_community_data['community_name'] == name].index:
        second_hand_community_data = second_hand_community_data.drop(idx)

total = pd.concat([second_hand_community_data, new_community_data], axis=0)
total = total.reset_index(drop=True)



idx_list = list(second_hand_community_data[second_hand_community_data['community_name'] == '北大资源燕南'].index)
idx = formed_lianjia_old[formed_lianjia_old['community_name'] == '联发公园里'].index