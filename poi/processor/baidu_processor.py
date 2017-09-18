import sys
sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')
import pandas as pd
import numpy as np
from constant import COMPLETE_DATA_HEADER_LIST, BAIDU_NAME_LIST


from dao.baidu_dao import format_baidu_poi_raw_data

class Baidu_Processor(object):
    def __init__(self, city_name):
        self.city_name = city_name
        
                
    def get_baidu_poi_conformed_raw_data(self):
        baidu_poi_raw_data = format_baidu_poi_raw_data(self.city_name)
        consolidated_poi = self.consolidate_second_hand_and_new_community_data_form(baidu_poi_raw_data)
        consolidated_poi['city'] = self.city_name
        consolidated_poi['data_type'] = 'baidu_poi'
        return consolidated_poi
    
    
    def consolidate_second_hand_and_new_community_data_form(self, baidu_raw_data):
        baidu_raw_data.rename(columns={'category': 'sub_category'}, inplace=True)    
        baidu_raw_data.rename(columns={'type': 'category'}, inplace=True)    
    
        header_to_add = [k for k in COMPLETE_DATA_HEADER_LIST if k not in BAIDU_NAME_LIST]
    
        column_num = len(header_to_add)
        row_num = len(baidu_raw_data)
        to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=header_to_add)
        consolidated_poi = pd.concat([baidu_raw_data, to_be_appended], axis=1)
        return consolidated_poi



