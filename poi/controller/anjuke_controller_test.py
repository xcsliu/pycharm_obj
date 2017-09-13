# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 15:03:25 2017

@author: xcsliu
"""
import pandas as pd
from dao.anjuke_dao import process_anjuke_new_community_raw_data, process_anjuke_second_hand_community_raw_data

city_name = '重庆'
anjuke_new = process_anjuke_new_community_raw_data(city_name)
anjuke_old = process_anjuke_second_hand_community_raw_data(city_name)

# ============
# 去重之后，会缺失index
tmp = anjuke_old.drop_duplicates(['truncate_name'])
# 重置index
tmp = tmp.reset_index(drop = True)
tmp = tmp.drop(['id'],axis=1)

name_list = ['build_type',
             'developer',
             'fitment_type',
             'house_types',
             'kaipan_new_date',
             'region_title',
             'sub_region_title']
for column_name in name_list:
    tmp[column_name] = None

# ===================================
second_hand_community_data = anjuke_old
new_community_data = anjuke_new
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
new_community_data = new_community_data.drop_duplicates(['loupan_name'])
new_community_data = new_community_data.reset_index(drop=True)

# 把新楼盘的column补齐
name_list_to_add_into_old_community_data = [ 'loupan_address',
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

for column_name in name_list_to_add_into_old_community_data:
    second_hand_community_data[column_name] = None
# 把旧楼盘的column补齐
name_list_to_add_into_new_community_data = [ 'community_id',
                                             'community_address',
                                             'community_mid_price',
                                             'community_mid_change',
                                             'community_lat',
                                             'community_lng',
                                             'community_prop_num']
for column_name in name_list_to_add_into_new_community_data:
    new_community_data[column_name] = None



# ===================================
# 把新楼盘中和旧楼盘重复名称的，直接将信息加到旧楼盘的信息里，然后记录下该楼盘的name
add_new_community_list = []
l = len(tmp)
for i in range(l):
    row = tmp.ix[i]
    name = row['truncate_name']
    if not anjuke_new[anjuke_new['loupan_name'] == name].empty:
        add_new_community_list.append(name)
        idx = anjuke_new[anjuke_new['loupan_name'] == name].index[0]
        for new_name in name_list:
            tmp[new_name][i] = anjuke_new.at[idx, new_name]
    
# 将剩下的新楼盘信息，编列并且加载在旧信息后面
tmp_anjuke_new = anjuke_new
for name in add_new_community_list:
    idx = anjuke_new[anjuke_new['loupan_name'] == name].index[0]
    tmp_anjuke_new = tmp_anjuke_new.drop(idx)


tmp_anjuke_new.rename(columns = {'loupan_name':'truncate_name', 
                                 'baidu_lat':'lat',
                                 'baidu_lng':'lng',
                                 'new_price':'mid_price'}, inplace = True)

tmp_anjuke_new = tmp_anjuke_new.drop(['loupan_id','metro_info'],axis=1)    
    
tmp_anjuke_new['mid_change'] = None


total = pd.concat([tmp_anjuke_new, tmp], axis = 0)
total = total.reset_index(drop = True)


# ==============================================================
name = row['truncate_name']
row = tmp.ix[15]
idx = anjuke_new[anjuke_new['loupan_name'] == '长帆时代公馆'].index[0]
for new_name in name_list:
    tmp[new_name][15] = anjuke_new.at[idx, new_name]



tmp.ix[5].loc['build_type'] = '多层'


type(tmp.at[2293,'mid_change'])


tmp.at[2293,'mid_change'] == None





anjuke_old[anjuke_old['truncate_name'] == '雍江翠湖']



lat_old = anjuke_old.at[ anjuke_old[anjuke_old['truncate_name'] == '恒大名都'].index[0], 'lat']

lng_old = anjuke_old.at[ anjuke_old[anjuke_old['truncate_name'] == '恒大名都'].index[0], 'lng']




lat_new = anjuke_new.at[ anjuke_new[anjuke_new['loupan_name'] == '恒大名都'].index[0], 'baidu_lat']

lng_new = anjuke_new.at[ anjuke_new[anjuke_new['loupan_name'] == '恒大名都'].index[0], 'baidu_lng']


# ============
anjuke_new.rename(columns = {'loupan_name':'truncate_name'}, inplace = True)
drop_anjuke_new = anjuke_new.drop(['prop_num'],axis=1)

merge_res = pd.merge(drop_anjuke_new, anjuke_old, on = 'truncate_name' )


# ============
# 去重
tmp = anjuke_old.drop_duplicates(['truncate_name'])


tmp_new = anjuke_new[:10]


