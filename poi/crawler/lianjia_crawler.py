import sys
if not '/home/xkool/poi/' in sys.path:
    sys.path.append('/home/xkool/poi/')

import json
import re
from json import JSONDecodeError
from requests import RequestException

from constant import lianjia_new_community_url_pattern, cq_url_for_lianjia_city_list, \
    lianjia_second_hand_community_url_pattern, THREAD_NUM, LIANJIA_SECOND_COMMUNITY_RAW_DATA_HEADER_LIST, \
    LIANJIA_SECOND_HAND_COMMUNITY_CITY_ID, lianjia_specific_second_hand_community_url_pattern, \
    LIANJIA_SPECIFIC_SECOND_COMMUNITY_READY_DATA_HEADER_LIST, lianjia_specific_new_community_url_pattern, \
    LIANJIA_SPECIFIC_NEW_COMMUNITY_CITY_NAME_LIST, LIANJIA_SPECIFIC_SECOND_HAND_COMMUNITY_CITY_NAME_LIST, CITY_LIST
from crawler.base_crawler import BaseCrawler
from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from util import get_raw_data_file_path, save_raw_data_in_tsv_file


class LianjiaCrawler(BaseCrawler):
    def __init__(self, city_name):
        super(LianjiaCrawler, self).__init__(city_name)
        self.lng, self.lat = self.get_city_center_lng_lat_by_city_name(self.city_name)
        self.rect_list = self.new_get_rect_list_by_lng_lat(self.lng, self.lat)
        self.new_community_data_num = 0
        self.second_hand_community_data_num_list = []

    def crawl_lianjia_raw_data(self):
        self.crawl_lianjia_second_hand_community_raw_data()
        self.crawl_lianjia_new_community_raw_data()

    def crawl_lianjia_new_community_raw_data(self):
        data_dict_list_for_new_community = []
        city_url = self.get_city_url_for_lianjia()
        if self.city_name in LIANJIA_SPECIFIC_NEW_COMMUNITY_CITY_NAME_LIST:
            community_data = self.get_specific_lianjia_new_community_data_with_url(city_url)
            community_data_list = community_data
            self.new_community_data_num = len(community_data_list)
            for community in community_data_list:
                data_dict_list_for_new_community.append(community)
        else:
            community_data = self.get_lianjia_new_community_data_with_url(city_url)
            community_data_list = community_data.values()
            for community_list in community_data_list:
                self.new_community_data_num += len(community_list)
                for community in community_list:
                    data_dict_list_for_new_community.append(community)

        file_path = get_raw_data_file_path(self.city_name,
                                           CrawlerDataType.RAW_DATA.value,
                                           CrawlerSourceName.LIANJIA.value,
                                           CrawlerDataLabel.NEW_COMMUNITY.value)
        save_raw_data_in_tsv_file(file_path, data_dict_list_for_new_community)
        self.logger.info('city : {} ][gross lianjia new community data : {}'.format(self.city_name,
                                                                                   self.new_community_data_num))

    def crawl_lianjia_second_hand_community_raw_data(self):
        self.crawl_with_thread_pool(THREAD_NUM,
                                    self.crawl_second_community_raw_data_with_rect,
                                    self.rect_list,
                                    self.write_second_community_raw_data_in_rect_to_file)
        self.logger.info('city : {} ][gross lianjia second hand data : {}'.format(self.city_name,
                                                                                  len(self.second_hand_community_data_num_list)))

    def crawl_second_community_raw_data_with_rect(self, rect):
        res = []
        if self.city_name in LIANJIA_SPECIFIC_SECOND_HAND_COMMUNITY_CITY_NAME_LIST:
            community_list = self.get_specific_lianjia_second_hand_community_list_with_rect(rect)
        else:
            community_list = self.get_lianjia_second_hand_community_list_with_rect(rect)
        for community in community_list:
            res.append(community)
            self.second_hand_community_data_num_list.append(1)
        return res

    def get_specific_lianjia_second_hand_community_list_with_rect(self, rect):
        rect_url = lianjia_specific_second_hand_community_url_pattern.format(rect[1], rect[3], rect[0], rect[2])
        try:
            response_text = self.get_response_text_with_url(rect_url)
        except RequestException as msg:
            self.logger.warning('[city name:{0}][exception:{1}][rect:{2}]'.format(self.city_name, msg, rect))
            return []
        try:
            text_json = json.loads(response_text)
        except JSONDecodeError as msg:
            self.logger.warning('[city name:{0}][exception:{1}][decode text:{2}]'.format(self.city_name, msg, response_text))
            return []
        if text_json and 'dataList' in text_json.keys():
            return text_json['dataList']
        return []

    def get_lianjia_second_hand_community_list_with_rect(self, rect):
        city_id = LIANJIA_SECOND_HAND_COMMUNITY_CITY_ID[self.city_name]
        rect_url = lianjia_second_hand_community_url_pattern.format(rect[0], rect[2], rect[1], rect[3], city_id)
        try:
            response_text = self.get_response_text_with_url(rect_url)
        except RequestException as msg:
            self.logger.warning('[city name:{0}][exception:{1}][rect:{2}]'.format(self.city_name, msg, rect))
            return []
        try:
            text_json = json.loads(response_text[43:-1])
        except JSONDecodeError as msg:
            self.logger.warning('[city name:{0}][exception:{1}][decode text:{2}]'.format(self.city_name, msg, response_text))
            return []
        if text_json and 'data' in text_json.keys():
            return text_json['data']
        return []

    def write_second_community_raw_data_in_rect_to_file(self, raw_data_list):
        write_file_path = get_raw_data_file_path(self.city_name,
                                                 CrawlerDataType.RAW_DATA.value,
                                                 CrawlerSourceName.LIANJIA.value,
                                                 CrawlerDataLabel.SECOND_HAND_COMMUNITY.value)
        header_list = LIANJIA_SPECIFIC_SECOND_COMMUNITY_READY_DATA_HEADER_LIST if self.city_name in LIANJIA_SPECIFIC_SECOND_HAND_COMMUNITY_CITY_NAME_LIST else LIANJIA_SECOND_COMMUNITY_RAW_DATA_HEADER_LIST
        self.write_to_file(header_list, write_file_path, raw_data_list)

    def get_lianjia_new_community_data_with_url(self, url):
        try:
            text = self.get_response_text_with_url(url)
        except RequestException as msg:
            self.logger.warning('[city name:{0}][exception:{1}][url:{2}]'.format(self.city_name, msg, url))
            return []
        try:
            data = json.loads(text[20:-1])
        except JSONDecodeError as msg:
            self.logger.warning('[city name:{0}][exception:{1}][decode text:{2}]'.format(self.city_name, msg, text))
            return []
        if data and 'data' in data.keys():
            return data['data']
        return []

    def get_specific_lianjia_new_community_data_with_url(self, url):
        try:
            text = self.get_response_text_with_url(url)
        except RequestException as msg:
            self.logger.warning('[city name:{0}][exception:{1}][url:{2}]'.format(self.city_name, msg, url))
            return []
        try:
            data = json.loads(text)
        except JSONDecodeError as msg:
            self.logger.warning('[city name:{0}][exception:{1}][decode text:{2}]'.format(self.city_name, msg, text))
            return []
        if data and 'dataList' in data.keys():
            return data['dataList']
        return []

    def get_city_url_for_lianjia(self):
        short_city_name = self.get_short_city_name_for_lianjia_new_community()
        if self.city_name in LIANJIA_SPECIFIC_NEW_COMMUNITY_CITY_NAME_LIST:
            city_url = lianjia_specific_new_community_url_pattern.format(short_city_name)
        else:
            city_url = lianjia_new_community_url_pattern.format(short_city_name)
        return city_url

    def get_short_city_name_for_lianjia_new_community(self):
        try:
            text =self.get_response_text_with_url(cq_url_for_lianjia_city_list)
        except RequestException as msg:
            self.logger.warning('[city name:{0}][exception:{1}]'.format(self.city_name, msg))
            raise RequestException
        pattern = re.compile('<li><a href="//(.*?).fang.lianjia.com/ditu/" data-xftrack="10140">(.*?)</a></li>')
        cities = re.findall(pattern, text)
        city_dict = {}
        for city in cities:
            city_dict[city[1]] = (city[0])
        city_dict['重庆'] = 'cq'
        if self.city_name in city_dict.keys():
            return city_dict[self.city_name]

if __name__ == '__main__':
    for city_name in CITY_LIST:
        crawler = LianjiaCrawler(city_name)
        crawler.crawl_lianjia_raw_data()
