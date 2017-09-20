import re
import pandas as pd

from constant import ANJUKE_SECOND_COMMUNITY_READY_DATA_HEADER_LIST, ANJUKE_NEW_COMMUNITY_READY_DATA_HEADER_LIST
from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from util import get_data_file_path
from xkool_date_util import XkDateUtil


def format_anjuke_raw_data(city_name):
    format_anjuke_new_community_raw_data(city_name)
    format_anjuke_second_hand_community_raw_data(city_name)


def format_anjuke_new_community_raw_data(city_name):
    xkool_date = XkDateUtil()
    read_file_path = get_data_file_path(city_name,
                                        CrawlerDataType.RAW_DATA.value,
                                        CrawlerSourceName.ANJUKE.value,
                                        CrawlerDataLabel.NEW_COMMUNITY.value,
                                        xkool_date.today_string)
    raw_data = pd.read_table(read_file_path, error_bad_lines=False)
    formed_raw_data = format_new_community_raw_data(raw_data)
    return formed_raw_data


def format_anjuke_second_hand_community_raw_data(city_name):
    xkool_date = XkDateUtil()
    read_file_path = get_data_file_path(city_name,
                                        CrawlerDataType.RAW_DATA.value,
                                        CrawlerSourceName.ANJUKE.value,
                                        CrawlerDataLabel.SECOND_HAND_COMMUNITY.value,
                                        xkool_date.today_string)
    raw_data = pd.read_table(read_file_path, error_bad_lines=False)
    formed_raw_data = format_second_community_raw_data(raw_data)
    return formed_raw_data


def format_second_community_raw_data(raw_data):
    formed_data = raw_data[ANJUKE_SECOND_COMMUNITY_READY_DATA_HEADER_LIST]
    return formed_data


def format_new_community_raw_data(raw_data):
    transfer_house_type(raw_data)
    ready_data = raw_data[ANJUKE_NEW_COMMUNITY_READY_DATA_HEADER_LIST]
    return ready_data


def transfer_house_type(raw_data):
    house_types = raw_data['house_types']
    pattern = re.compile("'alias': '(.*?)'.*?'area': '(.*?)',")
    for idx, house_type in enumerate(house_types):
        residence_info_ready = re.findall(pattern, house_type)
        house_types.loc[idx] = str(residence_info_ready)
