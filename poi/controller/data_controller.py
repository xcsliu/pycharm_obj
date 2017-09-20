import sys
sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')

import numpy as np
import pandas as pd
import os
import time
import json
from util import coordinate_distance

from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from processor.anjuke_processor import Anjuke_Processor
from processor.baidu_processor import Baidu_Processor

from processor.fangtianxia_processor import Fangtianxia_Processor

from processor.lianjia_processor import LianjiaProcessor
from util import get_data_file_path
from xkool_date_util import XkDateUtil


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

        lianjia_processor = LianjiaProcessor(self.city_name)
        lianjia_data = lianjia_processor.get_lianjia_conformed_raw_data()
        return anjuke_data, lianjia_data, baidu_data, fangtianxia_data


    def consolidate_community_data(self, lianjia_data, anjuke_data):
        community_added_index_list = []
        for index_lianjia, row_lianjia in lianjia_data.iterrows():
            # print(str('consolidate_community_data:') + str(idx_lianjia) + '/' + str(len(lianjia_data)))
            if not anjuke_data[anjuke_data['name'] == row_lianjia['name']].empty:                        # 是否有重复的小区名字
                for index_anjuke in anjuke_data[anjuke_data['name'] == row_lianjia['name']].index:       # 遍历整个重复的集合 
                    row_anjuke = anjuke_data.loc[index_anjuke]   
                    if coordinate_distance(row_anjuke['lng'], row_anjuke['lat'], row_lianjia['lng'], row_lianjia['lat']) < 2:  # 判断重合小区的距离，确定是否为同一小区                       
                        if type(row_lianjia['build_type']) == str and row_lianjia['build_type'] == '住宅' or type(row_lianjia['build_type']) == float and np.isnan(row_lianjia['build_type']): # 判断链家该小区是否为住宅
                            if index_lianjia not in community_added_index_list:
                                community_added_index_list.append(index_lianjia)     
                                merged_house_type = self.merge_house_type(anjuke_data.at[index_anjuke, 'house_type'], lianjia_data.at[index_lianjia, 'house_type'])
                                anjuke_data['house_type'][index_anjuke] = json.dumps(merged_house_type, ensure_ascii=False)               
                
            
                    
        # 链家去重
        for idx in community_added_index_list:
            lianjia_data = lianjia_data.drop(idx)

        lianjia_and_anjuke = pd.concat([lianjia_data, anjuke_data], axis=0)
        consolidated_community_data = lianjia_and_anjuke.reset_index(drop=True)
        return consolidated_community_data


    def consolidate_community_and_poi_data(self, community_data, poi_data):
        print ('consolidating community and poi data...')
        poi_added_in_community_index_list = []
        for index_community, row_community in community_data.iterrows():
            if not poi_data[poi_data['name'] == row_community['name']].empty:
                for index_poi in poi_data[poi_data['name'] == row_community['name']].index:       # 遍历整个重复的集合 
                    row_poi = poi_data.loc[index_poi]   
                    if coordinate_distance(row_poi['lng'], row_poi['lat'], row_community['lng'], row_community['lat']) < 2:
                        if index_poi not in poi_added_in_community_index_list:
                            poi_added_in_community_index_list.append(index_poi)
                            for header in ['uid', 'category', 'sub_category']:
                                community_data[header][index_community] = poi_data.at[index_poi, header]
        # poi 去重     
        for idx in poi_added_in_community_index_list:
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
        xkool_date = XkDateUtil()
        ready_data_file_path = get_data_file_path(self.city_name,
                                                  CrawlerDataType.READY_DATA.value,
                                                  CrawlerSourceName.ALL.value,
                                                  CrawlerDataLabel.TOTAL.value,
                                                  xkool_date.yesterday_string)
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
            for index_today, row_today in today_data.iterrows():
                print(str(index_today) + '/' + str(len(today_data)))

                if not yesterday_data[yesterday_data['uid'] == row_today['uid']].empty:
                    yesterday_data_series = yesterday_data[yesterday_data['uid'] == row_today['uid']]
                elif not yesterday_data[yesterday_data['name'] == row_today['name']].empty:
                    yesterday_data_series = yesterday_data[yesterday_data['name'] == row_today['name']]
                    
                for index_yesterday in yesterday_data_series.index:       # 遍历整个重复的集合 
                    row_yesterday = yesterday_data.loc[index_yesterday]   
                    if coordinate_distance(row_yesterday['lng'], row_yesterday['lat'], row_today['lng'], row_today['lat']) < 2:
                        if index_today not in today_in_yesterday_index_list:
                            today_in_yesterday_index_list.append(index_today)
                            # 合并户型信息
                            merged_house_type = self.merge_house_type(yesterday_data.at[index_yesterday, 'house_type'], today_data.at[index_today, 'house_type'])
                            yesterday_data['house_type'][index_yesterday] = json.dumps(merged_house_type, ensure_ascii=False) 
                            # 更新当前房价信息
                            updated_present_price = self.update_present_price()
                            yesterday_data['present_price'][index_yesterday] = updated_present_price
                        
            today_in_yesterday_index_list = list(set(today_in_yesterday_index_list))
            for idx in today_in_yesterday_index_list:
                today_data = today_data.drop(idx)

            total_ready_data = pd.concat([today_data, yesterday_data], axis=0)
            total_ready_data = total_ready_data.reset_index(drop=True)
            return total_ready_data


    def save_ready_data(self):
        xkool_date = XkDateUtil()
        ready_data = self.complement_ready_data()
        save_file_path  = get_data_file_path(self.city_name,
                                             CrawlerDataType.READY_DATA.value,
                                             CrawlerSourceName.ALL.value,
                                             CrawlerDataLabel.TOTAL.value,
                                             xkool_date.today_string)
        ready_data.to_csv(path_or_buf=save_file_path, sep='\t', index=False)



    def merge_house_type(self, A_input_house_type, B_input_house_type):
        A_house_type = json.loads( A_input_house_type )
        B_house_type = json.loads( B_input_house_type )
        merged_house_type = []
        for i in A_house_type:
            if i not in B_house_type:
                merged_house_type.append(i)
        merged_house_type += B_house_type
        return merged_house_type


    def update_present_price(self, today_present_price, yesterday_present_price):
        if type( today_present_price ) == float and np.isnan( today_present_price ):
            res_price = yesterday_present_price
        else:
            res_price = today_present_price
        return res_price



if __name__ == '__main__':
    start = time.time()
    controller = Data_Controller('重庆')
    
    anjuke_data, lianjia_data, baidu_data, fangtianxia_data = controller.get_raw_data_from_diff_source()
    consolidated_community_data = controller.consolidate_community_data(lianjia_data, anjuke_data)
    # consolidated_community_and_poi_data = controller.consolidate_community_and_poi_data(consolidated_community_data, baidu_data)
    # total_consolidated_raw_data = controller.consolidate_land_data_and_rest(fangtianxia_data, consolidated_community_and_poi_data)
    # controller.save_ready_data()
    end = time.time()
    print (end-start)


# ==========================
start = time.time()
controller = Data_Controller('重庆')
# consolidated_community_data = controller.consolidate_community_data(lianjia_data, anjuke_data)
# consolidated_community_and_poi_data = controller.consolidate_community_and_poi_data(consolidated_community_data, baidu_data)
# total_consolidated_raw_data = controller.consolidate_land_data_and_rest(fangtianxia_data, consolidated_community_and_poi_data)


xkool_date = XkDateUtil()
ready_data = total_consolidated_raw_data
save_file_path  = get_data_file_path(controller.city_name,
                                     CrawlerDataType.READY_DATA.value,
                                     CrawlerSourceName.ALL.value,
                                     CrawlerDataLabel.TOTAL.value,
                                     xkool_date.today_string)
ready_data.to_csv(path_or_buf=save_file_path, sep='\t', index=False)

end = time.time()
print (end-start)
# ==========================
'''
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
        
 


row = lianjia_data[lianjia_data['name'] == '康田西宸中心']['house_type']
house_type = row.at[row.index[0]]

pattern_1 = re.compile('(\d{1,})居')
pattern_2 = re.compile('套内 (.*?)m²')
pattern_3 = re.compile('(\d{1,})')

res_1 = re.findall(pattern_1, house_type)
res_2 = re.findall(pattern_2, house_type)
if res_2:
    res_3 = re.findall(pattern_3, res_2[0])  
else:
    res_3 = []
res = [res_1, res_3]
res = [[int(room_num) for room_num in res[0]], [int(area) for area in res[1]]]


max_room_num, min_room_num = max(res[0]), min(res[0])
max_area, min_area = res[1][1], res[1][0]
unit_area = (max_area - min_area) / ( max_room_num - min_room_num )
for mid_room_num in res[0][1:-1]:
    res[1].append( int((mid_room_num - min_room_num)*unit_area + min_area))
res[1].sort()    
res[0].sort()    

def room_num_and_area_2_house_type(room_num, area):
    if room_num == 1:
        room_type = '{}室1厅'
    else:
        room_type = '{}室2厅'
    return (room_type.format(room_num), str(area))


tmp = []
for index, room_num in enumerate(res[0]):
    tmp.append( room_num_and_area_2_house_type(room_num, res[1][index]) )



def get_consolidate_house_type(house_type):  
    def room_num_and_area_2_house_type(room_num, area):
        if room_num == 1 or area < 45:
            room_type = '{}室1厅'
        else:
            room_type = '{}室2厅'
        return (room_type.format(room_num), str(area))
    
    if type( house_type ) == float:
        return str([])
    
    
    pattern_1 = re.compile('(\d{1,})居')
    pattern_2 = re.compile('套内 (.*?)m²')
    pattern_3 = re.compile('(\d{1,})')
    
    res_1 = re.findall(pattern_1, house_type)
    res_2 = re.findall(pattern_2, house_type)
    if res_2:
        res_3 = re.findall(pattern_3, res_2[0])  
    else:
        res_3 = []
    res = [res_1, res_3]
    res = [[int(room_num) for room_num in res[0]], [int(area) for area in res[1]]]
    
    if not res[0]:
        return str([])
    
    elif len(res[0]) > 1 :
        max_room_num, min_room_num = max(res[0]), min(res[0])
        max_area, min_area = res[1][1], res[1][0]
        unit_area = (max_area - min_area) / ( max_room_num - min_room_num )
        for mid_room_num in res[0][1:-1]:
            res[1].append( int((mid_room_num - min_room_num)*unit_area + min_area))
    elif res[0] and not res[1]:
        res[1] = [i*38 for i in res[0]]
        
        
    res[1].sort()    
    res[0].sort()    
    tmp = []
    for index, room_num in enumerate(res[0]):
        tmp.append( room_num_and_area_2_house_type(room_num, res[1][index]) )
    return str(tmp)

house_type_list = [house_type_1,house_type_2,house_type_3,house_type_4,house_type_5]


test_res = [get_consolidate_house_type(house_type) for house_type in house_type_list]



     
        




for index, row in lianjia_data.iterrows():
    lianjia_data['house_type'][index] = get_consolidate_house_type( lianjia_data.at[index, 'house_type'] )
       
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

aa = json.s(a)

row.loc['house_type']

# ================
pattern = re.compile('pointY = "(.*?)";')
lat = re.findall(pattern, text)[0]
# ================



    

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


import json
row = anjuke_data[anjuke_data['name'] == '同天依云郡']['house_type']
house_type_anjuke = row.at[row.index[0]]
res_json_anjuke = json.loads(house_type_anjuke)


row = lianjia_data[lianjia_data['name'] == '逸翠庄园君玺']['house_type']
house_type_lianjia = row.at[row.index[0]]
res_json_lianjia = json.loads(house_type_lianjia)

house_type = house_type.replace('(','[').replace(')',']').replace("'",'"')



import json
a = '[["4室2厅2卫","325"], ["5室2厅2卫","239"],["5室3厅2卫","235"]]'
b = '[("4室2厅2卫","325"), ("5室2厅2卫","239"),("5室3厅2卫","235")]'
aa = json.loads(a)
bb = json.loads(str([]))



def room_num_and_area_2_house_type(room_num, area):
    if room_num == 1 or area < 45:
        room_type = '{}室1厅'
    else:
        room_type = '{}室2厅'
    res = [room_type.format(room_num), str(area)]
    return res


res = room_num_and_area_2_house_type(2,70)
tmp = [res,res]
json_res = str(tmp).replace("'", '"')



anjuke_house_type = json.loads( house_type_anjuke )
lianjia_house_type = json.loads( house_type_lianjia )

merged_house_type = []
for i in anjuke_house_type:
    if i not in lianjia_house_type:
        merged_house_type.append(i)
merged_house_type += lianjia_house_type
        
bb = json.dumps(merged_house_type, ensure_ascii=False)

for index, row in total_consolidated_raw_data.iterrows():
    print ( type(row['present_price']) )


'''