import sys
if not '/home/xkool/poi/' in sys.path:
    sys.path.append('/home/xkool/poi/')

import re
from bs4 import BeautifulSoup
from requests import RequestException

from constant import fangtianxia_page_url_pattern, FANGTIANXIA_CITY_NUM_TRANSFER, fangtianxia_parcel_url_pattern, \
    THREAD_NUM, FANGTIANXIA_PARCEL_RAW_DATA_HEADER_LIST, CITY_LIST
from crawler.base_crawler import BaseCrawler
from crawler.crawler_enum import CrawlerDataType, CrawlerSourceName, CrawlerDataLabel
from util import get_raw_data_file_path


class FangtianxiaCrawler(BaseCrawler):
    def __init__(self, city_name):
        super(FangtianxiaCrawler, self).__init__(city_name)
        self.url_list = self.get_parcel_url_list()

    def crawl_fangtianxia_parcel_raw_data(self):
        self.crawl_with_thread_pool(THREAD_NUM,
                                    self.get_parcel_raw_data_with_parcel_url,
                                    self.url_list,
                                    self.write_parcel_raw_data_in_rect_to_file)
        self.logger.info('city : {} ][gross fangtianxia parcel data : {}'.format(self.city_name,
                                                                                   len(self.url_list)))

    def get_parcel_raw_data_with_parcel_url(self, parcel_url):
        try:
            text = self.get_response_text_with_url(parcel_url)
        except RequestException as msg:
            self.logger.warning('[city name:{0}][exception:{1}][parcel:{2}]'.format(self.city_name, msg, parcel_url))
            return []
        if text:
            soup = BeautifulSoup(text, "lxml")
            parcel_data = {}
            # 基础信息&交易信息
            for data_part_index in range(2):
                for detail_data in soup.select('table[class="tablebox02 mt10"]')[data_part_index].select('td'):
                    key_content = detail_data.contents[0].string[:-1]
                    value_content = detail_data.contents[1].string
                    parcel_data[key_content] = value_content
            # 经纬度信息+地块编号
            pattern = re.compile('pointX = "(.*?)";')
            lng = re.findall(pattern, text)[0]
            parcel_data['lng'] = lng

            pattern = re.compile('pointY = "(.*?)";')
            lat = re.findall(pattern, text)[0]
            parcel_data['lat'] = lat

            pattern = re.compile('地块编号：(.*?)</span>')
            num_of_parcel = re.findall(pattern, text)[0]
            parcel_data['地块编号'] = num_of_parcel
            return [parcel_data]

    def get_parcel_url_list(self):
        page_size = self.get_page_size(self.city_name)
        parcel_url_list = []
        for page_num in range(1, page_size + 1):
            url = fangtianxia_page_url_pattern.format(FANGTIANXIA_CITY_NUM_TRANSFER[self.city_name], page_num)
            try:
                text = self.get_response_text_with_url(url)
            except RequestException as msg:
                self.logger.warning(
                    '[city name:{0}][exception:{1}][page num:{2}]'.format(self.city_name, msg, page_num))
                return []
            soup = BeautifulSoup(text, "lxml")
            for i in soup.select('h3'):
                parcel_url = fangtianxia_parcel_url_pattern + i.contents[1]['href']
                parcel_url_list.append(parcel_url)
        return parcel_url_list

    def get_page_size(self, city_name):
        city_name_num = FANGTIANXIA_CITY_NUM_TRANSFER[city_name]
        url = fangtianxia_page_url_pattern.format(str(city_name_num), '1')
        try:
            text = self.get_response_text_with_url(url)
        except Exception as msg:
            self.logger.warning('[city name:{0}][exception:{1}]'.format(self.city_name, msg))
            return 0
        pattern = re.compile('</a><span>1/(.*?)</span><a class="paga28')
        if re.findall(pattern, text):
            page_size = re.findall(pattern, text)[0]
            return int(page_size)
        return 0


    def write_parcel_raw_data_in_rect_to_file(self, raw_data_list):
        write_file_path = get_raw_data_file_path(self.city_name,
                                                 CrawlerDataType.RAW_DATA.value,
                                                 CrawlerSourceName.FANGTIANXIA.value,
                                                 CrawlerDataLabel.PARCEL.value)
        self.write_to_file(FANGTIANXIA_PARCEL_RAW_DATA_HEADER_LIST, write_file_path, raw_data_list)

if __name__ == '__main__':
    for city_name in CITY_LIST:
        crawler = FangtianxiaCrawler(city_name)
        crawler.crawl_fangtianxia_parcel_raw_data()
