import sys
if not '/home/xkool/poi/' in sys.path:
    sys.path.append('/home/xkool/poi/')

import json
from json import JSONDecodeError
from pypinyin import lazy_pinyin
from requests import RequestException

from constant import anjuke_new_community_url_pattern, anjuke_2nd_community_url_pattern, THREAD_NUM, \
    ANJUKE_NEW_COMMUNITY_RAW_DATA_HEADER_LIST, ANJUKE_SECOND_COMMUNITY_RAW_DATA_HEADER_LIST, \
    ANJUKE_NEW_COMMUNITY_CITY_ID, CITY_LIST
from crawler.base_crawler import BaseCrawler
from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from util import get_raw_data_file_path


class AnjukeCrawler(BaseCrawler):
    def __init__(self, city_name):
        super(AnjukeCrawler, self).__init__(city_name)
        self.lng, self.lat = self.get_city_center_lng_lat_by_city_name(self.city_name)
        self.rect_list = self.new_get_rect_list_by_lng_lat(self.lng, self.lat)
        self.new_community_data_num_list = []
        self.second_hand_community_data_num_list = []

    def crawl_anjuke_raw_data(self):
        self.crawl_anjuke_second_hand_community_raw_data()
        self.crawl_anjuke_new_community_raw_data()

    def crawl_anjuke_new_community_raw_data(self):
        self.crawl_with_thread_pool(THREAD_NUM,
                                    self.crawl_new_community_raw_data_with_rect,
                                    self.rect_list,
                                    self.write_new_community_raw_data_in_rect_to_file)
        self.logger.info('city : {} ][gross anjuke new community data : {}'.format(self.city_name, len(self.new_community_data_num_list)))

    def crawl_anjuke_second_hand_community_raw_data(self):
        self.crawl_with_thread_pool(THREAD_NUM,
                                    self.crawl_second_community_raw_data_with_rect,
                                    self.rect_list,
                                    self.write_second_community_raw_data_in_rect_to_file)
        self.logger.info('city : {} ][gross anjuke second hand data : {}'.format(self.city_name, len(self.second_hand_community_data_num_list)))

    def crawl_new_community_raw_data_with_rect(self, rect):
        res = []
        community_list = self.get_anjuke_new_community_list_with_rect(rect)
        for community in community_list:
            res.append(community)
            self.new_community_data_num_list.append(1)
        return res

    def crawl_second_community_raw_data_with_rect(self, rect):
        res = []
        community_list = self.get_anjuke_second_hand_community_list_with_rect(rect)
        for community in community_list:
            res.append(community)
            self.second_hand_community_data_num_list.append(1)
        return res

    def get_anjuke_new_community_list_with_rect(self, rect):
        city_id = ANJUKE_NEW_COMMUNITY_CITY_ID[self.city_name]
        rect_url = anjuke_new_community_url_pattern.format(city_id, *rect)
        try:
            response_text = self.get_response_text_with_url(rect_url)
        except RequestException as msg:
            self.logger.warning('[city name:{0}][exception:{1}][rect:{2}][url:{3}]'.format(self.city_name, msg, rect, rect_url))
            return []
        try:
            content = json.loads(response_text[43:-1])
        except JSONDecodeError as msg:
            self.logger.warning(
                '[city name:{0}][exception:{1}][rect:{2}][decode text:{3}]'.format(self.city_name, msg, rect, response_text))
            return []
        if content and 'result' in content:
            text = content['result']['rows']
            return text
        return []

    def get_anjuke_second_hand_community_list_with_rect(self, rect):
        rect_url = self.get_anjuke_second_hand_community_list_url(rect)
        try:
            response_text = self.get_response_text_with_url(rect_url)
        except RequestException as msg:
            self.logger.warning('[city name:{0}][exception:{1}][rect:{2}]'.format(self.city_name, msg, rect))
            return []
        try:
            content = json.loads(response_text)
        except JSONDecodeError as msg:
            self.logger.warning(
                '[city name:{0}][exception:{1}][rect:{2}][decode text:{3}]'.format(self.city_name, msg, rect,
                                                                                   response_text))
            return []
        if content and 'val' in content:
                text = content['val']['comms']
                return text
        return []

    def get_anjuke_second_hand_community_list_url(self, rect):
        city_name_pinyin = ''.join(lazy_pinyin(self.city_name))
        url = anjuke_2nd_community_url_pattern.format(city_name_pinyin, rect[1], rect[3], rect[0], rect[2])
        return url

    def write_new_community_raw_data_in_rect_to_file(self, raw_data_list):
        write_file_path = get_raw_data_file_path(self.city_name,
                                                 CrawlerDataType.RAW_DATA.value,
                                                 CrawlerSourceName.ANJUKE.value,
                                                 CrawlerDataLabel.NEW_COMMUNITY.value)
        self.write_to_file(ANJUKE_NEW_COMMUNITY_RAW_DATA_HEADER_LIST, write_file_path, raw_data_list)

    def write_second_community_raw_data_in_rect_to_file(self, raw_data_list):
        write_file_path = get_raw_data_file_path(self.city_name,
                                                 CrawlerDataType.RAW_DATA.value,
                                                 CrawlerSourceName.ANJUKE.value,
                                                 CrawlerDataLabel.SECOND_HAND_COMMUNITY.value)
        self.write_to_file(ANJUKE_SECOND_COMMUNITY_RAW_DATA_HEADER_LIST, write_file_path, raw_data_list)


if __name__ == '__main__':
    for city_name in CITY_LIST:
        crawler = AnjukeCrawler(city_name)
        crawler.crawl_anjuke_raw_data()
