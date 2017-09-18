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
                if not yesterday_data[yesterday_data['uid'] == row_today['uid']].empty:
                    idx_yesterday = yesterday_data[yesterday_data['uid'] == row_today['uid']].index[0]
                    today_in_yesterday_index_list.append(idx_today)
                    for header in ['present_price']:
                        if today_data.at[idx_today, header] and not np.isnan(today_data.at[idx_today, header]):
                            yesterday_data[header][idx_yesterday] = today_data.at[idx_today, header]
                    for header in ['house_type']:
                        yesterday_data[header][idx_yesterday] = str(yesterday_data.at[idx_yesterday, header]) + ',' + str(today_data.at[idx_today, header])

                # 合并楼盘部分
                '''
                if not tmp_res.empty:
                    for index_new, row_new in tmp_res.iterrows():  
                        if coordinate_distance(row_old['lng'], row_old['lat'], row_new['lng'], row_new['lat']) < 2:
                            old_community_index_list_to_drop.append(index_old)
                        
                            for header in ['present_price', 'prop_num']:
                                new_community_data[header][index_new] = second_hand_community_data.at[index_old, header]
    
                '''





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
    controller.save_ready_data()
    end = time.time()
    print (end-start)
    
'''
anjuke_data, lianjia_data, baidu_data, fangtianxia_data = controller.get_raw_data_from_diff_source()

controller.save_ready_data()





'''
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




