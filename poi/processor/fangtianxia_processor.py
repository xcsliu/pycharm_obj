import sys
sys.path.append('E:\\xcsliu_project\\pycharm_obj\\poi')
import pandas as pd
import numpy as np
from constant import COMPLETE_DATA_HEADER_LIST, FANGTIANXIA_NAME_LIST


from dao.fangtianxia_dao import format_fangtianxia_parcel_raw_data

class Fangtianxia_Processor(object):
    def __init__(self, city_name):
        self.city_name = city_name
        
                
    def get_fangtianxia_conformed_raw_data(self):
        fangtianxia_raw_data = format_fangtianxia_parcel_raw_data(self.city_name)
        consolidated_land_data = self.consolidate_land_data(fangtianxia_raw_data)
        consolidated_land_data['city'] = self.city_name
        consolidated_land_data['data_type'] = 'land'
        return consolidated_land_data
    
    
    def consolidate_land_data(self, land_raw_data):
        land_raw_data.rename(columns={'地区': 'city',
                                      '总面积': 'total_area',
                                      '建设用地面积': 'construction_land_area',
                                      '规划建筑面积': 'planned_land_area',
                                      '容积率': 'floor_area_ratio',
                                      '绿化率': 'green_ratio',
                                      '商业比例': 'business_ratio',
                                      '建筑密度': 'building_density',
                                      '限制高度': 'height_limit',
                                      '出让年限': 'time_limit',
                                      '位置':'address',
                                      '规划用途': 'planned_use',
                                      '起始日期': 'start_date',
                                      '起始价': 'start_price',
                                      '地块编号': 'land_number',
                                      '四至': 'name',
                                      '出让年限': 'time_limit'}, inplace=True)     
        land_raw_data_with_drop = land_raw_data.drop(['出让形式','成交价','楼面地价','溢价率'],axis = 1)
        
        header_to_add = [k for k in COMPLETE_DATA_HEADER_LIST if k not in FANGTIANXIA_NAME_LIST]
    
        column_num = len(header_to_add)
        row_num = len(land_raw_data_with_drop)
        to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=header_to_add)
        consolidated_land_data = pd.concat([land_raw_data_with_drop, to_be_appended], axis=1)
        return consolidated_land_data
    
