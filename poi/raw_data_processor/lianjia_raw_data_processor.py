import pandas as pd

from constant import LIANJIA_NEW_COMMUNITY_READY_DATA_HEADER_LIST, LIANJIA_SECOND_COMMUNITY_READY_DATA_HEADER_LIST
from crawler.crawler_enum import CrawlerSourceName, CrawlerDataLabel, CrawlerDataType
from util import get_raw_data_file_path


def process_lianjia_raw_data(city_name):
    process_lianjia_new_community_raw_data(city_name)
    process_lianjia_second_hand_community_raw_data(city_name)

def process_lianjia_new_community_raw_data(city_name):
    read_file_path = get_raw_data_file_path(city_name,
                                            CrawlerDataType.RAW_DATA.value,
                                            CrawlerSourceName.LIANJIA.value,
                                            CrawlerDataLabel.NEW_COMMUNITY.value)
    save_file_path = get_raw_data_file_path(city_name,
                                            CrawlerDataType.READY_DATA.value,
                                            CrawlerSourceName.LIANJIA.value,
                                            CrawlerDataLabel.NEW_COMMUNITY.value)
    raw_data = pd.read_table(read_file_path, error_bad_lines=False)
    ready_data = process_new_community_raw_data_to_ready(raw_data)
    ready_data.to_csv(path_or_buf=save_file_path, sep='\t', encoding='utf-8')

def process_lianjia_second_hand_community_raw_data(city_name):
    read_file_path = get_raw_data_file_path(city_name,
                                            CrawlerDataType.RAW_DATA.value,
                                            CrawlerSourceName.LIANJIA.value,
                                            CrawlerDataLabel.SECOND_HAND_COMMUNITY.value)
    save_file_path = get_raw_data_file_path(city_name,
                                            CrawlerDataType.READY_DATA.value,
                                            CrawlerSourceName.LIANJIA.value,
                                            CrawlerDataLabel.SECOND_HAND_COMMUNITY.value)
    raw_data = pd.read_table(read_file_path, error_bad_lines=False)
    ready_data = process_second_hand_community_raw_data_to_ready(raw_data)
    ready_data.to_csv(path_or_buf=save_file_path, sep='\t', encoding='utf-8')

def process_new_community_raw_data_to_ready(raw_data):
    ready_data = raw_data[LIANJIA_NEW_COMMUNITY_READY_DATA_HEADER_LIST]
    return ready_data

def process_second_hand_community_raw_data_to_ready(raw_data):
    ready_data = raw_data[LIANJIA_SECOND_COMMUNITY_READY_DATA_HEADER_LIST]
    return ready_data

if __name__ == '__main__':
    process_lianjia_raw_data('重庆')