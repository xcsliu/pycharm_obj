import sys

from util import coordinate_distance

sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')

from constant import COMPLETE_DATA_HEADER_LIST, ANJUKE_SECOND_HAND_COMMUNITY_NAME_LIST, \
    ANJUKE_NEW_COMMUNITY_NAME_LIST
from dao.anjuke_dao import format_anjuke_new_community_raw_data, format_anjuke_second_hand_community_raw_data

# =====================
import numpy as np
import pandas as pd


class Anjuke_Processor(object):
    def __init__(self, city_name):
        self.city_name = city_name

    def get_anjuke_conformed_raw_data(self):
        anjuke_old, anjuke_new = self.get_anjuke_community_raw_data()
        consolidated_old, consolidated_new = self.consolidate_second_hand_and_new_community_data_form(anjuke_old, anjuke_new)
        conformed_raw_data = self.merge_community_raw_data(consolidated_old, consolidated_new)
        conformed_raw_data['city'] = self.city_name
        conformed_raw_data['data_type'] = 'anjuke_community'
        return conformed_raw_data

    def get_anjuke_community_raw_data(self):
        anjuke_new = format_anjuke_new_community_raw_data(self.city_name)
        anjuke_old = format_anjuke_second_hand_community_raw_data(self.city_name)
        return anjuke_old, anjuke_new

    def consolidate_second_hand_and_new_community_data_form(self, second_hand_community_data, new_community_data):
        # rename and drop
        second_hand_community_data.rename(columns={'truncate_name': 'name',
                                                   'mid_price': 'present_price'}, inplace=True)
        second_hand_community_data_with_drop = second_hand_community_data.drop(['id', 'mid_change'], axis=1)
        second_hand_community_data_with_drop = second_hand_community_data_with_drop.drop_duplicates(['name','lat','lng'])

        new_community_data.rename(columns={'loupan_name': 'name',
                                           'prop_num': 'prop_num',
                                           'baidu_lat': 'lat',
                                           'baidu_lng': 'lng',
                                           'new_price': 'start_price',
                                           'region_title': 'region',
                                           'sub_region_title': 'sub_region',
                                           'house_types': 'house_type',
                                           'kaipan_new_date': 'start_date'}, inplace=True)
        new_community_data_with_drop = new_community_data.drop(['loupan_id', 'metro_info'], axis=1)
        new_community_data_with_drop = new_community_data_with_drop.drop_duplicates(['name','lat','lng'])

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

    def merge_community_raw_data(self, second_hand_community_data, new_community_data):
        # 把两个数据集重叠的部分整合在一起
        print ('merging anjuke community raw data...')
        old_community_index_list_to_drop = []
        # 遍历二手房
        for index_old, row_old in second_hand_community_data.iterrows():
            print(str(index_old) + '/' + str(len(second_hand_community_data)))
            # 如果二手房的小区名称在新房中出现
            tmp_res = new_community_data[new_community_data['name'] == row_old['name']]
            if not tmp_res.empty:
                for index_new, row_new in tmp_res.iterrows():  
                    if coordinate_distance(row_old['lng'], row_old['lat'], row_new['lng'], row_new['lat']) < 2:
                        old_community_index_list_to_drop.append(index_old)
                    
                        for header in ['present_price', 'prop_num']:
                            new_community_data[header][index_new] = second_hand_community_data.at[index_old, header]
        # 把重叠的部分从二手房数据集中去除
        for index in old_community_index_list_to_drop:
            second_hand_community_data = second_hand_community_data.drop(index)
        # 把两部分数据集拼合在一起
        total = pd.concat([new_community_data, second_hand_community_data], axis=0)
        total = total.reset_index(drop=True)
        return total


if __name__ == '__main__':
    processor = Anjuke_Processor('重庆')
    anjuke_old, anjuke_new = processor.get_anjuke_community_raw_data()
    consolidated_old, consolidated_new = processor.consolidate_second_hand_and_new_community_data_form(anjuke_old, anjuke_new)
    conformed_raw_data = processor.merge_community_raw_data(consolidated_old, consolidated_new)
    conformed_raw_data['city'] = processor.city_name
    conformed_raw_data['data_type'] = 'anjuke_community'
    
    
 



'''  
row_list = []
for index, row in conformed_raw_data[conformed_raw_data['name'] == '25小时'].iterrows():
    row_list.append(row)
print ( coordinate_distance(row_list[0]['lng'], row_list[0]['lat'], row_list[1]['lng'], row_list[1]['lat']) )
    

added_new_community_index_list = []
# 遍历二手房
for index_A, row_A in consolidated_old.iterrows():
    print(str(index_A) + '/' + str(len(consolidated_old)))
    # 如果二手房的小区名称在新房中出现
    tmp_res = consolidated_new[consolidated_new['name'] == row_A['name']]
    if not tmp_res.empty:
        for index_B, row_B in tmp_res.iterrows():  
            if coordinate_distance(row_A['lng'], row_A['lat'], row_B['lng'], row_B['lat']) < 2:
                added_new_community_index_list.append(index_B)








  
tmp_list = []
drop_duplicated_old_with_name = anjuke_old.drop_duplicates(['name','lat','lng'])
for i, row in anjuke_old.iterrows():
    print (row.index())


drop_duplicated_old_with_id = anjuke_old.drop_duplicates(['id'])
    
    
drop_duplicated_old_with_name.index 
    
d_list = list(drop_duplicated_old_with_name.index )    
total_list = [i for i in range(len(anjuke_old))]
res = [k for k in total_list if k not in d_list]


name_list = []
for i,k in anjuke_old.iterrows():
    if i in res:
        name_list.append(k['name'])

duplicated_list = []
for k in name_list:
    duplicated_list.append(anjuke_old[anjuke_old['name'] == k])
    print (anjuke_old[anjuke_old['name'] == k])
l = []
for i,k in anjuke_old[anjuke_old['name'] == '海缘阁'].iterrows():
    print (k)
    l.append(k)
'''