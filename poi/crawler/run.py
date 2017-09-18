from constant import CITY_LIST
from crawler.anjuke_crawler import AnjukeCrawler
from crawler.baidu_crawler import BaiduCrawler
from crawler.fangtianxia_crawler import FangtianxiaCrawler
from crawler.lianjia_crawler import LianjiaCrawler

if __name__ == '__main__':
    city_name = '重庆'
    # for city_name in CITY_LIST:
    print ('crawling {} city for anjuke'.format(city_name))
    crawler = AnjukeCrawler(city_name)
    crawler.crawl_anjuke_raw_data()
    print('crawling {} city for lianjia'.format(city_name))
    crawler = LianjiaCrawler(city_name)
    crawler.crawl_lianjia_raw_data()
    print('crawling {} city for baidu'.format(city_name))
    crawler = BaiduCrawler(city_name)
    crawler.crawl_baidu_raw_data()
    print('crawling {} city for fangtianxia'.format(city_name))
    crawler = FangtianxiaCrawler(city_name)
    crawler.crawl_fangtianxia_parcel_raw_data()
