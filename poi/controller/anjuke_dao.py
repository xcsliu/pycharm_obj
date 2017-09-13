import re
import pandas as pd

from constant import ANJUKE_NEW_COMMUNITY_READY_DATA_HEADER_LIST, ANJUKE_SECOND_COMMUNITY_READY_DATA_HEADER_LIST
from crawler.crawler_enum import CrawlerSourceName, CrawlerDataLabel, CrawlerDataType
from util import get_raw_data_file_path


def process_anjuke_raw_data(city_name):
    process_anjuke_new_community_raw_data(city_name)
    process_anjuke_second_hand_community_raw_data(city_name)

def process_anjuke_new_community_raw_data(city_name):
    read_file_path = get_raw_data_file_path(city_name,
                                            CrawlerDataType.RAW_DATA.value,
                                            CrawlerSourceName.ANJUKE.value,
                                            CrawlerDataLabel.NEW_COMMUNITY.value)
    raw_data = pd.read_table(read_file_path, error_bad_lines=False)
    ready_data = process_new_community_raw_data_to_ready(raw_data)
    return ready_data

def process_anjuke_second_hand_community_raw_data(city_name):
    read_file_path = get_raw_data_file_path(city_name,
                                            CrawlerDataType.RAW_DATA.value,
                                            CrawlerSourceName.ANJUKE.value,
                                            CrawlerDataLabel.SECOND_HAND_COMMUNITY.value)
    raw_data = pd.read_table(read_file_path, error_bad_lines=False)
    ready_data = process_second_community_raw_data_to_ready(raw_data)
    return ready_data

def process_second_community_raw_data_to_ready(raw_data):
    ready_data = raw_data[ANJUKE_SECOND_COMMUNITY_READY_DATA_HEADER_LIST]
    return ready_data

def process_new_community_raw_data_to_ready(raw_data):
    transfer_house_type(raw_data)
    ready_data = raw_data[ANJUKE_NEW_COMMUNITY_READY_DATA_HEADER_LIST]
    return ready_data

def transfer_house_type(raw_data):
    house_types = raw_data['house_types']
    pattern = re.compile("'alias': '(.*?)'.*?'area': '(.*?)',")
    for idx, house_type in enumerate(house_types):
        residence_info_ready = re.findall(pattern, house_type)
        house_types.loc[idx] = str(residence_info_ready)
