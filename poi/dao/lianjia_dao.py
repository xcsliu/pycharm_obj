import pandas as pd

from constant import LIANJIA_NEW_COMMUNITY_READY_DATA_HEADER_LIST, LIANJIA_SECOND_COMMUNITY_READY_DATA_HEADER_LIST
from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from util import get_data_file_path, get_today_date


def format_lianjia_raw_data(city_name):
    format_lianjia_new_community_raw_data(city_name)
    format_lianjia_second_hand_community_raw_data(city_name)


def format_lianjia_new_community_raw_data(city_name):
    date = get_today_date()
    read_file_path = get_data_file_path(city_name,
                                        CrawlerDataType.RAW_DATA.value,
                                        CrawlerSourceName.LIANJIA.value,
                                        CrawlerDataLabel.NEW_COMMUNITY.value,
                                        date)
    raw_data = pd.read_table(read_file_path, error_bad_lines=False)
    formed_raw_data = format_new_community_raw_data(raw_data)
    return formed_raw_data


def format_lianjia_second_hand_community_raw_data(city_name):
    date = get_today_date()
    read_file_path = get_data_file_path(city_name,
                                        CrawlerDataType.RAW_DATA.value,
                                        CrawlerSourceName.LIANJIA.value,
                                        CrawlerDataLabel.SECOND_HAND_COMMUNITY.value,
                                        date)
    raw_data = pd.read_table(read_file_path, error_bad_lines=False)
    formed_raw_data = format_second_hand_community_raw_data(raw_data)
    return formed_raw_data


def format_new_community_raw_data(raw_data):
    formed_data = raw_data[LIANJIA_NEW_COMMUNITY_READY_DATA_HEADER_LIST]
    return formed_data


def format_second_hand_community_raw_data(raw_data):
    formed_data = raw_data[LIANJIA_SECOND_COMMUNITY_READY_DATA_HEADER_LIST]
    return formed_data
