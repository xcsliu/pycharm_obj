import pandas as pd
import numpy as np

from constant import SUBWAY_STATION_HEADER_LIST, COMPLETE_DATA_HEADER_LIST
from dao.subway_dao import SubwayDao


class SubwayProcessor:
    def __init__(self, city_name):
        self.city_name = city_name
        self.subway_station_dao = SubwayDao(city_name)

    def get_subway_station_conformed_data(self):
        subway_data = self.consolidate_subway_station_conformed_raw_data()
        subway_data['category'] = 'subway_station'
        subway_data['house_type'] = '[]'
        return subway_data

    def consolidate_subway_station_conformed_raw_data(self):
        subway_station_raw_data = self.subway_station_dao.format_lianjia_second_hand_community_raw_data()
        subway_station_raw_data.rename(columns={'line_name': 'sub_category',
                                                'latitude': 'lat',
                                                'longitude': 'lng'}, inplace=True)
        subway_station_raw_data_with_drop = subway_station_raw_data.drop(['id', 'order_no'], axis=1)
        header_to_add = [header for header in COMPLETE_DATA_HEADER_LIST if header not in SUBWAY_STATION_HEADER_LIST]

        column_num = len(header_to_add)
        row_num = len(subway_station_raw_data)
        to_be_appended = pd.DataFrame([[np.nan] * column_num] * row_num, columns=header_to_add)
        consolidated_data = pd.concat([subway_station_raw_data_with_drop, to_be_appended], axis=1)
        return consolidated_data
