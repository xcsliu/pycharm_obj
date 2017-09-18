import sys

sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')
import pandas as pd
import numpy as np

from constant import COMPLETE_DATA_HEADER_LIST, LIANJIA_SECOND_HAND_COMMUNITY_NAME_LIST, LIANJIA_NEW_COMMUNITY_NAME_LIST
from dao.lianjia_dao import format_lianjia_new_community_raw_data, format_lianjia_second_hand_community_raw_data


class Lianjia_Processor(object):
    def __init__(self, city_name):
        self.city_name = city_name

    def get_lianjia_conformed_raw_data(self):
        anjuke_old, anjuke_new = self.get_lianjia_community_raw_data()
        consolidated_old, consolidated_new = self.consolidate_second_hand_and_new_community_data_form(anjuke_old, anjuke_new)
        conformed_raw_data = self.merge_community_raw_data(consolidated_old, consolidated_new)
        conformed_raw_data['city'] = self.city_name
        conformed_raw_data['data_type'] = 'lianjia_community'
        return conformed_raw_data

    def get_lianjia_community_raw_data(self):
        lianjia_new = format_lianjia_new_community_raw_data(self.city_name)
        lianjia_old = format_lianjia_second_hand_community_raw_data(self.city_name)
        return lianjia_old, lianjia_new

    def consolidate_second_hand_and_new_community_data_form(self, second_hand_community_data, new_community_data):
        # rename
        second_hand_community_data.rename(columns={'avg_unit_price': 'present_price',
                                                   'bs_avg_unit_price': 'altra_present_price',
                                                   'house_count': 'prop_num',
                                                   'latitude': 'lat',
                                                   'longitude': 'lng'}, inplace=True)
        for i, row in second_hand_community_data.iterrows():
            if np.isnan(second_hand_community_data.at[i, 'present_price']):
                second_hand_community_data['present_price'][i] = second_hand_community_data.at[i, 'altra_present_price']
        second_hand_community_data_with_drop = second_hand_community_data.drop(
            ['id', 'altra_present_price', 'min_price_total'], axis=1)

        new_community_data.rename(columns={'resblock_name': 'name',
                                           'house_type': 'build_type',
                                           'latitude': 'lat',
                                           'longitude': 'lng',
                                           'average_price': 'start_price',
                                           'resblock_frame_area': 'loupan_frame_area'}, inplace=True)
        new_community_data.rename(columns={'rooms': 'house_type'}, inplace=True)

        for i, row in new_community_data.iterrows():
            if type(new_community_data.at[i, 'house_type']) != str and type(
                    new_community_data.at[i, 'loupan_frame_area']) != str:
                pass
            elif type(new_community_data.at[i, 'house_type']) != str:
                new_community_data['house_type'][i] = new_community_data.at[i, 'loupan_frame_area']
            elif type(new_community_data.at[i, 'loupan_frame_area']) != str:
                pass
            else:
                new_community_data['house_type'][i] = new_community_data.at[i, 'house_type'] + ',' + \
                                                      new_community_data.at[i, 'loupan_frame_area']

        new_community_data_with_drop = new_community_data.drop(
            ['resblock_id', 'min_frame_area', 'max_frame_area', 'loupan_frame_area'], axis=1)

        # compliment old community
        old_header_to_add = [k for k in COMPLETE_DATA_HEADER_LIST if k not in LIANJIA_SECOND_HAND_COMMUNITY_NAME_LIST]
        column_num = len(old_header_to_add)
        row_num = len(second_hand_community_data)
        to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=old_header_to_add)
        consolidated_old = pd.concat([second_hand_community_data_with_drop, to_be_appended], axis=1)

        # compliment new community
        new_header_to_add = [k for k in COMPLETE_DATA_HEADER_LIST if k not in LIANJIA_NEW_COMMUNITY_NAME_LIST]
        column_num = len(new_header_to_add)
        row_num = len(new_community_data)
        to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=new_header_to_add)
        consolidated_new = pd.concat([new_community_data_with_drop, to_be_appended], axis=1)

        return consolidated_old, consolidated_new

    def merge_community_raw_data(self, second_hand_community_data, new_community_data):
        # 把两个数据集重叠的部分小区信息整合在一起
        print('merging lianjia community raw data...')
        added_old_community_name_list = []
        for i, row in new_community_data.iterrows():
            name = row['name']
            build_type = row['build_type']
            if not second_hand_community_data[second_hand_community_data['name'] == name].empty:
                if build_type == '住宅':
                    added_old_community_name_list.append(name)
                    idx = second_hand_community_data[second_hand_community_data['name'] == name].index[0]
                    for new_name in ['present_price', 'prop_num']:
                        new_community_data[new_name][i] = second_hand_community_data.at[idx, new_name]
        # 在旧楼盘数据集中去掉已经填充过的部分
        num_note = 0
        for name in added_old_community_name_list:
            # num_note += 1
            # print(num_note)
            for idx in second_hand_community_data[second_hand_community_data['name'] == name].index:
                second_hand_community_data = second_hand_community_data.drop(idx)

        total = pd.concat([second_hand_community_data, new_community_data], axis=0)
        total = total.reset_index(drop=True)
        return total



















