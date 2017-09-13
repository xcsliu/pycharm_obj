import numpy as np
import pandas as pd
import os
from constant import ANJUKE_SECOND_HAND_COMMUNITY_NAME_LIST_TO_ADD, ANJUKE_NEW_COMMUNITY_NAME_LIST_TO_ADD, \
    ANJUKE_UPDATE_HEADER_LIST
from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from dao.anjuke_dao import format_anjuke_new_community_raw_data, format_anjuke_second_hand_community_raw_data
from util import get_ready_data_file_path


def get_anjuke_community_raw_data(city_name):
    anjuke_new = format_anjuke_new_community_raw_data(city_name)
    anjuke_old = format_anjuke_second_hand_community_raw_data(city_name)
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
    column_num = len(ANJUKE_SECOND_HAND_COMMUNITY_NAME_LIST_TO_ADD)
    row_num = len(second_hand_community_data)
    to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num,
                                  columns=ANJUKE_SECOND_HAND_COMMUNITY_NAME_LIST_TO_ADD)
    consolidated_old = pd.concat([second_hand_community_data, to_be_appended], axis=1)

    for column_name in ANJUKE_SECOND_HAND_COMMUNITY_NAME_LIST_TO_ADD:
        second_hand_community_data[column_name] = np.nan

    # compliment new community
    column_num = len(ANJUKE_NEW_COMMUNITY_NAME_LIST_TO_ADD)
    row_num = len(new_community_data)
    to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=ANJUKE_NEW_COMMUNITY_NAME_LIST_TO_ADD)
    consolidated_new = pd.concat([new_community_data, to_be_appended], axis=1)

    for column_name in ANJUKE_NEW_COMMUNITY_NAME_LIST_TO_ADD:
        new_community_data[column_name] = np.nan
    return consolidated_old, consolidated_new


def merge_community_raw_data(second_hand_community_data, new_community_data):
    # 把两个数据集重叠的部分整合在一起
    added_new_community_name_list = []
    for i in range(len(new_community_data)):
        print(str(i) + '/' + str(len(new_community_data)))
        row = new_community_data.iloc[i]
        name = row['community_name']
        if not second_hand_community_data[second_hand_community_data['community_name'] == name].empty:
            added_new_community_name_list.append(name)
            idx = second_hand_community_data[second_hand_community_data['community_name'] == name].index[0]
            for new_name in ANJUKE_SECOND_HAND_COMMUNITY_NAME_LIST_TO_ADD:
                second_hand_community_data[new_name][idx] = new_community_data.at[i, new_name]
    # 把重叠的部分从新楼盘数据集中去除
    for name in added_new_community_name_list:
        idx = new_community_data[new_community_data['community_name'] == name].index[0]
        new_community_data = new_community_data.drop(idx)
    # 把两部分数据集拼合在一起
    total = pd.concat([new_community_data, second_hand_community_data], axis=0)
    total = total.reset_index(drop=True)
    return total


def compliment_raw_data_into_ready_data(raw_data, ready_data):
    added_raw_data_name_list = []
    for k in range(len(ready_data)):
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


def process_and_save(city_name):
    anjuke_old, anjuke_new = get_anjuke_community_raw_data(city_name)
    formed_anjuke_old, formed_anjuke_new = consolidate_form(anjuke_old, anjuke_new)
    merged_raw_data = merge_community_raw_data(formed_anjuke_old, formed_anjuke_new)

    ready_data_file_path = get_ready_data_file_path(city_name,
                                                    CrawlerDataType.READY_DATA.value,
                                                    CrawlerSourceName.ANJUKE.value,
                                                    CrawlerDataLabel.SECOND_HAND_COMMUNITY.value)

    if os.path.exists(ready_data_file_path):
        ready_data = pd.read_table(ready_data_file_path, error_bad_lines=False)
        processed_data = compliment_raw_data_into_ready_data(merged_raw_data, ready_data)
        processed_data.to_csv(path_or_buf=ready_data_file_path, sep='\t', encoding='utf-8')
    else:
        merged_raw_data.to_csv(path_or_buf=ready_data_file_path, sep='\t', encoding='utf-8')

