import sys
sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')
import pandas as pd
import numpy as np

from constant import COMPLETE_DATA_HEADER_LIST, LIANJIA_SECOND_HAND_COMMUNITY_NAME_LIST, LIANJIA_NEW_COMMUNITY_NAME_LIST
from dao.lianjia_dao import format_lianjia_new_community_raw_data, format_lianjia_second_hand_community_raw_data
from util import coordinate_distance


class Lianjia_Processor(object):
    def __init__(self, city_name):
        self.city_name = city_name


    def get_lianjia_conformed_raw_data(self):
        lianjia_old, lianjia_new = self.get_lianjia_community_raw_data()
        consolidated_old, consolidated_new = self.consolidate_second_hand_and_new_community_data_form(lianjia_old, lianjia_new)
        conformed_raw_data = self.merge_community_raw_data(consolidated_old, consolidated_new)
        conformed_raw_data['city'] = self.city_name
        conformed_raw_data['data_type'] = 'community'
        return conformed_raw_data


    def get_lianjia_community_raw_data(self):
        lianjia_new = format_lianjia_new_community_raw_data(self.city_name)
        lianjia_old = format_lianjia_second_hand_community_raw_data(self.city_name)
        return lianjia_old, lianjia_new


    def consolidate_second_hand_and_new_community_data_form(self, second_hand_community_data, new_community_data):
        # rename
        second_hand_community_data.rename(columns={'avg_unit_price': 'present_price',
                                                   'bs_avg_unit_price': 'reserve_present_price',
                                                   'house_count': 'prop_num',
                                                   'latitude': 'lat',
                                                   'longitude': 'lng'}, inplace=True)
        for i, row in second_hand_community_data.iterrows():
            if np.isnan(second_hand_community_data.at[i, 'present_price']):
                second_hand_community_data['present_price'][i] = second_hand_community_data.at[i, 'reserve_present_price']
        second_hand_community_data_with_drop = second_hand_community_data.drop(['id',
                                                                                'reserve_present_price',
                                                                                'min_price_total'], axis=1)
        second_hand_community_data_with_drop = second_hand_community_data_with_drop.drop_duplicates(['name','lat','lng'])

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

        new_community_data_with_drop = new_community_data.drop(['resblock_id',
                                                                'min_frame_area',
                                                                'max_frame_area',
                                                                'loupan_frame_area'], axis=1)
        new_community_data_with_drop = new_community_data.drop_duplicates(['name','build_type'])

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
        old_community_index_list_to_drop = []
        for new_index, row_new in new_community_data.iterrows():
            if not second_hand_community_data[second_hand_community_data['name'] == row_new['name']].empty:
                if row_new['build_type'] == '住宅':
                    for index_old, row_old in second_hand_community_data[second_hand_community_data['name'] == row_new['name']].iterrows():
                        if coordinate_distance(row_old['lng'], row_old['lat'], row_new['lng'], row_new['lat']) < 2:
                            old_community_index_list_to_drop.append(index_old)
                            for header in ['present_price', 'prop_num']:
                                new_community_data[header][new_index] = second_hand_community_data.at[index_old, header]
        # 在旧楼盘数据集中去掉已经填充过的部分
        for index in old_community_index_list_to_drop:
            second_hand_community_data = second_hand_community_data.drop(index)

        total = pd.concat([second_hand_community_data, new_community_data], axis=0)
        total = total.reset_index(drop=True)
        return total




if __name__ == '__main__':
    processor = Lianjia_Processor('重庆')
    lianjia_old, lianjia_new = processor.get_lianjia_community_raw_data()
    consolidated_old, consolidated_new = processor.consolidate_second_hand_and_new_community_data_form(lianjia_old, lianjia_new)
    conformed_raw_data = processor.merge_community_raw_data(consolidated_old, consolidated_new)
    conformed_raw_data['city'] = processor.city_name
    conformed_raw_data['data_type'] = 'community'


'''
consolidated_new_with_drop = consolidated_old.drop_duplicates(['name'])


index_drop_list = list(consolidated_new_with_drop.index)



for i in range(833):
    if i not in index_drop_list:
        print (i)



consolidated_old[consolidated_old['name'] == '保利山庄']


coordinate_distance(29.570888,106.510148,29.573813,106.511168)

'''