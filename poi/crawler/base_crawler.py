import sys
if not '/home/xkool/poi/' in sys.path:
    sys.path.append('/home/xkool/poi/')
import os
from multiprocessing.pool import ThreadPool
import requests
import tablib
from requests import RequestException
from retrying import retry

from constant import THREAD_NUM, STEP_NUM, UNIT_DISTANCE, city_center_url_pattern, BAIDU_API_AK, TIMEOUT, HEADERS
from logger import FinalLogger


class BaseCrawler(object):
    def __init__(self, city_name, thread_num=THREAD_NUM, step_num=STEP_NUM, unit_distance=UNIT_DISTANCE):
        self.city_name = city_name
        self.thread_num = thread_num
        self.step_num = step_num
        self.unit_distance = unit_distance
        self.logger = FinalLogger.getLogger()

    def get_city_center_lng_lat_by_city_name(self, city_name):
        city_url = city_center_url_pattern.format(city_name, BAIDU_API_AK)
        try:
            response = requests.get(city_url, timeout=TIMEOUT)
            response_dict = response.json()
            location = response_dict['result']['location']
            return location['lng'], location['lat']
        except RequestException as msg:
            self.logger.warning('[city name:{0}][exception:{1}]'.format(self.city_name, msg))
            raise ConnectionError

    @retry(stop_max_attempt_number=10)
    def get_response_text_with_url(self, url):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        return None

    def new_get_rect_list_by_lng_lat(self, center_lng, center_lat):
        rect_list = []
        start_point_lng = center_lng - self.step_num * self.unit_distance / 2
        start_point_lat = center_lat - self.step_num * self.unit_distance / 2
        for idx_in_lng in range(self.step_num):
            lower_left_lng = start_point_lng + idx_in_lng * self.unit_distance
            for idx_in_lat in range(self.step_num):
                lower_left_lat = start_point_lat + idx_in_lat * self.unit_distance
                rect_list.append(['%.6f' % (lower_left_lng),
                                  '%.6f' % (lower_left_lat),
                                  '%.6f' % (lower_left_lng + self.unit_distance),
                                  '%.6f' % (lower_left_lat + self.unit_distance)])
        return rect_list

    def crawl_with_thread_pool(self, thread_num, func_in_thread, input_list, func_to_callback):
        pool = ThreadPool(processes=thread_num)
        for i in range( len(input_list) ):
            async_result = pool.apply_async(func_in_thread, (input_list[i],), callback=func_to_callback)
        pool.close()
        pool.join()

    def write_to_file(self, header, file_path, raw_data_list):
        for raw_data in raw_data_list:
            raw_data_value_list = []
            for key_name in header:
                if key_name not in raw_data.keys():
                    raw_data[key_name] = 'nan'
                raw_data_value_list.append(raw_data[key_name])

            data_value = tablib.Dataset(raw_data_value_list)
            data_key = tablib.Dataset(header)
            if not os.path.exists(file_path):
                with open(file_path, 'a+', encoding='utf-8') as f:
                    f.write(str(data_key.tsv))
                    f.write(str(data_value.tsv))
            else:
                with open(file_path, 'a+', encoding='utf-8') as f:
                    f.write(str(data_value.tsv))
