import pandas as pd

from constant import FANGTIANXIA_READY_HEADER_LIST
from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from util import get_data_file_path, get_today_date


def format_fangtianxia_parcel_raw_data(city_name):
    date = get_today_date()
    read_file_path = get_data_file_path(city_name,
                                        CrawlerDataType.RAW_DATA.value,
                                        CrawlerSourceName.FANGTIANXIA.value,
                                        CrawlerDataLabel.PARCEL.value,
                                        date)
    raw_data = pd.read_table(read_file_path, error_bad_lines=False)
    formed_raw_data = format_raw_data(raw_data)
    return formed_raw_data


def format_raw_data(raw_data):
    ready_data = raw_data[FANGTIANXIA_READY_HEADER_LIST]
    return ready_data