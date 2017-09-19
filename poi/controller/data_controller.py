import sys
sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')

import numpy as np
import pandas as pd
import os
import time

from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from processor.anjuke_processor import Anjuke_Processor
from processor.baidu_processor import Baidu_Processor

from processor.fangtianxia_processor import Fangtianxia_Processor

from processor.lianjia_processor import Lianjia_Processor
from util import get_data_file_path, get_yesterday_date, get_today_date


class Data_Controller():
    def __init__(self, city_name):
        self.city_name = city_name

    def get_raw_data_from_diff_source(self):
        baidu_processor = Baidu_Processor(self.city_name)
        baidu_data = baidu_processor.get_baidu_poi_conformed_raw_data()

        anjuke_processor = Anjuke_Processor(self.city_name)
        anjuke_data = anjuke_processor.get_anjuke_conformed_raw_data()

        fangtianxia_processor = Fangtianxia_Processor(self.city_name)
        fangtianxia_data = fangtianxia_processor.get_fangtianxia_conformed_raw_data()

        lianjia_processor = Lianjia_Processor(self.city_name)
        lianjia_data = lianjia_processor.get_lianjia_conformed_raw_data()
        return anjuke_data, lianjia_data, baidu_data, fangtianxia_data


    def consolidate_community_data(self, lianjia_data, anjuke_data):
        community_added_index_list = []
        for idx_lianjia, row in lianjia_data.iterrows():
            # print(str('consolidate_community_data:') + str(idx_lianjia) + '/' + str(len(lianjia_data)))
            name = row['name']
            build_type = row['build_type']
            if not anjuke_data[anjuke_data['name'] == name].empty:
                if type(build_type) == str and build_type == '住宅' or type(build_type) == float and np.isnan(build_type):
                    idx_anjuke = anjuke_data[anjuke_data['name'] == name].index[0]
                    community_added_index_list.append(idx_lianjia)
                    for new_name in ['house_type']:
                        anjuke_data[new_name][idx_anjuke] = str(anjuke_data.at[idx_anjuke, new_name]) + ',' + str(
                            lianjia_data.at[idx_lianjia, new_name])
        # 链家去重
        for idx in community_added_index_list:
            lianjia_data = lianjia_data.drop(idx)

        lianjia_and_anjuke = pd.concat([lianjia_data, anjuke_data], axis=0)
        consolidated_community_data = lianjia_and_anjuke.reset_index(drop=True)
        return consolidated_community_data


    def consolidate_community_and_poi_data(self, community_data, poi_data):
        print ('consolidating community and poi data...')
        poi_in_community_index_list = []
        for idx, row in community_data.iterrows():
            # print(str('consolidate_community_and_poi_data:') + str(idx) + '/' + str(len(community_data)))
            name = row['name']
            if not poi_data[poi_data['name'] == name].empty:
                idx_baidu = poi_data[poi_data['name'] == name].index[0]
                poi_in_community_index_list.append(idx_baidu)
                for new_name in ['uid', 'category', 'sub_category']:
                    community_data[new_name][idx] = poi_data.at[idx_baidu, new_name]

        poi_in_community_index_list = list(set(poi_in_community_index_list))
        for idx in poi_in_community_index_list:
            poi_data = poi_data.drop(idx)

        baidu_and_community = pd.concat([poi_data, community_data], axis=0)
        baidu_and_community = baidu_and_community.reset_index(drop=True)
        return baidu_and_community



    def consolidate_land_data_and_rest(self, land_data, community_and_poi):
        total = pd.concat([land_data, community_and_poi], axis=0)
        total_consolidated_raw_data = total.reset_index(drop=True)
        return total_consolidated_raw_data


    def get_today_data(self):
        anjuke_data, lianjia_data, baidu_data, fangtianxia_data = self.get_raw_data_from_diff_source()
        consolidated_community_data = self.consolidate_community_data(lianjia_data, anjuke_data)
        baidu_and_community = self.consolidate_community_and_poi_data(consolidated_community_data, baidu_data)
        total_consolidated_raw_data = self.consolidate_land_data_and_rest(fangtianxia_data, baidu_and_community)
        return total_consolidated_raw_data


    def get_yesterday_ready_data(self):
        yesterday = get_yesterday_date()
        ready_data_file_path = get_data_file_path(self.city_name,
                                                  CrawlerDataType.READY_DATA.value,
                                                  CrawlerSourceName.ALL.value,
                                                  CrawlerDataLabel.TOTAL.value,
                                                  yesterday)
        if not os.path.exists(ready_data_file_path):
            return None
        yesterday_data = pd.read_table(ready_data_file_path, error_bad_lines=False)
        return yesterday_data


    def complement_ready_data(self):
        yesterday_data = self.get_yesterday_ready_data()
        today_data = self.get_today_data()

        if not yesterday_data:
            return today_data
        else:
            today_in_yesterday_index_list = []
            for idx_today, row_today in today_data.iterrows():
                print(str(idx_today) + '/' + str(len(today_data)))

                # 合成有 uid 的部分,主要是合成 baidu 部分
                # 这部分信息有两类，一类是 community 一类是 baidu_poi，
                # community 部分主要是更新其价格，补充户型信息；
                # baidu_poi 信息可以直接更新 or 舍弃，因为基本上没有需要更新的内容
                if not yesterday_data[yesterday_data['uid'] == row_today['uid']].empty:
                    idx_yesterday = yesterday_data[yesterday_data['uid'] == row_today['uid']].index[0]
                    today_in_yesterday_index_list.append(idx_today)
                    for header in ['present_price']:
                        if today_data.at[idx_today, header] and not np.isnan(today_data.at[idx_today, header]):
                            yesterday_data[header][idx_yesterday] = today_data.at[idx_today, header]
                    for header in ['house_type']:
                        yesterday_data[header][idx_yesterday] = str(yesterday_data.at[idx_yesterday, header]) + ',' + str(today_data.at[idx_today, header])


            today_in_yesterday_index_list = list(set(today_in_yesterday_index_list))
            for idx in today_in_yesterday_index_list:
                today_data = today_data.drop(idx)

            total_ready_data = pd.concat([today_data, yesterday_data], axis=0)
            total_ready_data = total_ready_data.reset_index(drop=True)
            return total_ready_data


    def save_ready_data(self):
        today = get_today_date()
        ready_data = self.complement_ready_data()
        save_file_path  = get_data_file_path(self.city_name,
                                             CrawlerDataType.READY_DATA.value,
                                             CrawlerSourceName.ALL.value,
                                             CrawlerDataLabel.TOTAL.value,
                                             today)
        ready_data.to_csv(path_or_buf=save_file_path, sep='\t', index=False)



 


if __name__ == '__main__':
    start = time.time()
    controller = Data_Controller('重庆')
    
    anjuke_data, lianjia_data, baidu_data, fangtianxia_data = controller.get_raw_data_from_diff_source()
    # controller.save_ready_data()
    end = time.time()
    print (end-start)






import json
row = anjuke_data[anjuke_data['name'] == '翡翠御园']['house_type']

row = row.replace('(','[').replace(')',']').replace("'",'"')

row_loads = json.loads(row)


# =安居客====================
# 将没有信息的部分规范为 []
for index, row in anjuke_data.iterrows():
    if type( row['house_type'] ) == float:
        anjuke_data['house_type'][index] = '[]'
# 将有信息的部分，规范为可以 loads 的格式
for index, row in anjuke_data.iterrows():
    if row['house_type'] != '[]':
        anjuke_data['house_type'][index] = row['house_type'].replace('(','[').replace(')',']').replace("'",'"')



# =链家===============
# 规范成一个统一的数据格式：
# house_type 规范成为 str
import re
for index, row in lianjia_data.iterrows():
    if type( row['house_type'] ) == float:
        lianjia_data['house_type'][index] = ''
        
 


row = lianjia_data[lianjia_data['name'] == '民生路']['house_type']
house_type = row.at[row.index[0]]

pattern_1 = re.compile('(\d)居')
pattern_2 = re.compile('套内 (.*?)m²')
pattern_3 = re.compile('(\d{1,})')

res_1 = re.findall(pattern_1, house_type)
res_2 = re.findall(pattern_2, house_type)
if res_2:
    res_3 = re.findall(pattern_3, res_2[0])  
else:
    res_3 = []
res = [res_1, res_3]


     
        

pattern_1 = re.compile('(\d)居')
pattern_2 = re.compile('套内 (.*?)m²')
pattern_3 = re.compile('(\d{1,})')
for index, row in lianjia_data.iterrows():
    res_1 = re.findall(pattern_1, row['house_type'])
    res_2 = re.findall(pattern_2, row['house_type'])
    if res_2:
        res_3 = re.findall(pattern_3, res_2[0])  
    else:
        res_3 = []
    lianjia_data['house_type'][index] = [res_1, res_3]
       
# 提取居室信息
tmp_house_num_list = []




# 居室数目







row = lianjia_data[lianjia_data['name'] == '翡翠御园']['house_type']
house_type = row.at[1181]


for index, row in lianjia_data.iterrows():
    if type( row['house_type'] ) == float:
        lianjia_data['house_type'][index] = ''


# =====
# 统计下户型信息
k = 0
for index, row in anjuke_data.iterrows():
    if type(row['house_type']) == float:
        k += 1


k = 0
for index, row in lianjia_data.iterrows():
    if type(row['house_type']) == float:
        k += 1


a = [["4室2厅2卫","325"], ["5室2厅2卫","239"],["5室3厅2卫","235"]]

a_json = '[]'

aa = json.loads(a_json)

row.loc['house_type']

# ================
pattern = re.compile('pointY = "(.*?)";')
lat = re.findall(pattern, text)[0]
# ================



    
'''
anjuke_data, lianjia_data, baidu_data, fangtianxia_data = controller.get_raw_data_from_diff_source()

controller.save_ready_data()


前一天和当天的信息整合：
1.会有部分新的poi信息
2.会有部分楼盘有更新的 present price 和 house type，前者进行更新，后者进行补充；
3.想办法将链家的部分楼盘的户型信息进行格式化，写作 (几室几厅,面积) 的形式








read_path = 'E:\\xcsliu_project\\pycharm_obj\\poi\\poi_data\\chongqing\\ready_data\\2017_09_18\\chongqing_insensitive_source_total_data_2017_09_18.tsv'

raw_data = pd.read_table(read_path, error_bad_lines=False, encoding = 'gbk')




def get_surrounding_total_data(city_name, lng, lat, width_KM):
    ready_data = raw_data
    dif_lat, dif_lng = get_per_km_with_lat_lng(lat, lng, width_KM)
    new_data = ready_data[(ready_data['lat'] > lat - dif_lat )&
                          (ready_data['lat'] < lat + dif_lat )&
                          (ready_data['lng'] > lng - dif_lng )&
                          (ready_data['lng'] < lng + dif_lng)]
    return new_data

'''


