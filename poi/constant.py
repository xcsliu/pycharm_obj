# crawler config for thread with rect list
TIMEOUT = 5
STEP_NUM = 20
UNIT_DISTANCE = 0.005
THREAD_NUM = 30

# city list
CITY_LIST = ['重庆', '北京', '上海', '广州', '深圳', '天津', '成都', '长沙', '南京', '杭州']

# headers
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

# baidu
# BAIDU_API_AK = 'GEPiAH9zkDx5oy4K1Vj7Znw8zmbGhY0M' # by Shen
BAIDU_API_AK = '0yMQoetZ3YOogQyAjr7CcUPBzCT82yBp'  # by xkool
BAIDU_POI_CATEGORIES = ['美食$餐厅$超市$酒店$公园$酒吧$咖啡厅$小吃$茶座', '购物中心$便利店$园区$厂矿', '商铺$地铁$公交$轻轨$停车场$火车站$机场', '金融$住宅$美容$娱乐$健身',
                        '幼儿园$小学$中学$大学$教育$学校', '医疗$政府机构$公司$文化$数码$银行$写字楼$汽车']
city_center_url_pattern = 'https://source.map.baidu.com/geocoder/v2/?address={}&output=json&ak={}'
baidu_poi_url_pattern =  'https://source.map.baidu.com/place/v2/search?query={}&scope=2&coord_type=1&bounds={}&output=json&ak={}'
BAIDU_POI_RAW_DATA_HEADER_LIST = ['name', 'location', 'address', 'telephone', 'uid', 'street_id', 'detail', 'detail_info']
BAIDU_POI_READY_DATA_HEADER_LIST = ['name', 'uid', 'lat', 'lng', 'category', 'type']

# anjuke
anjuke_2nd_community_url_pattern = 'https://{}.anjuke.com/v3/ajax/map/sale/facet/?room_num=-1&price_id=-1&area_id=-1&floor=-1&orientation=-1&is_two_years=0&is_school=0&is_metro=0&order_id=0&p=1&zoom=19&' \
                                   'lat={}_{}&lng={}_{}&kw=&maxp=99'
anjuke_new_community_url_pattern = 'https://source.fang.anjuke.com/web/loupan/mapNewlist/?city_id={}&callback=jQuery1113006248457428238563_1502272365154&zoom=16&' \
                                   'swlng={}&swlat={}&nelng={}&nelat={}&' \
                                   'order=rank&order_type=asc&region_id=0&sub_region_id=0&house_type=0&property_type=0&price_id=0&' \
                                   'bunget_id=0&status_sale=3%2C4%2C6%2C7%2C5&price_title=%E5%85%A8%E9%83%A8&keywords=&page=1&page_size=500&timestamp=29&_=1502272365159'
ANJUKE_NEW_COMMUNITY_RAW_DATA_HEADER_LIST = ['tags', 'spinyin', 'price', 'new_price_desc', 'new_price', 'new_price_unit', 'loupan_id',
                                             'status_sale','loupan_name','loupan_name_short','address','region','region_title',
                                             'sub_region_id','sub_region_title','fitment_type','build_type','metro_info','lat','lng',
                                             'baidu_lat','baidu_lng','kaipan_date','kaipan_new_date','phone_400_main','phone_400_ext',
                                             'sale_tag', 'default_image', 'is_recd', 'loupan_link', 'tuangou', 'fanli', 'house_type_count',
                                             'house_types', 'house_type_recommend', 'kft', 'is_sales_market', 'is_sales_promotion',
                                             'is_customer_train', 'developer', 'dongtai', 'prop_num']
ANJUKE_NEW_COMMUNITY_READY_DATA_HEADER_LIST = ['address', 'baidu_lat', 'baidu_lng', 'build_type', 'developer',
                                               'fitment_type', 'house_types', 'kaipan_new_date', 'loupan_id',
                                               'loupan_name', 'metro_info', 'new_price', 'prop_num', 'region_title',
                                               'sub_region_title']

ANJUKE_SECOND_COMMUNITY_RAW_DATA_HEADER_LIST = ['build_type', 'fitment_type', 'house_type', 'start_price', 'mid_change', 'lat', 'lng', 'prop_num']
ANJUKE_SECOND_COMMUNITY_READY_DATA_HEADER_LIST = ['truncate_name', 'id', 'address', 'mid_price', 'mid_change', 'lat', 'lng', 'prop_num']

ANJUKE_NEW_COMMUNITY_CITY_ID = {'北京': 14,
                                '上海': 11,
                                '重庆': 20,
                                '深圳': 13,
                                '广州': 12,
                                '天津': 17,
                                '成都': 15,
                                '长沙': 27,
                                '南京': 16,
                                '杭州': 18,
                                '武汉': 22,
                                '西安': 31,
                                '厦门': 46}

ANJUKE_NEW_COMMUNITY_NAME_LIST = ['name',
                                  'lat',
                                  'lng',
                                  'address',
                                  'build_type',
                                  'fitment_type',
                                  'house_type',
                                  'start_price',
                                  'region',
                                  'sub_region',
                                  'prop_num',
                                  'developer',
                                  'start_date']

ANJUKE_SECOND_HAND_COMMUNITY_NAME_LIST = ['name',
                                          'address',
                                          'lat',
                                          'lng',
                                          'prop_num',
                                          'present_price']

ANJUKE_UPDATE_HEADER_LIST = ['community_mid_price','community_mid_change','community_prop_num','loupan_prop_num','loupan_price']


# lianjia
lianjia_new_community_url_pattern = 'http://{}.fang.lianjia.com/xinfang/mapsearchloupan?&&callback=speedupjsonpapi&_=1502246125390'
lianjia_specific_new_community_url_pattern = 'http://{}.fang.lianjia.com/loupan/ajax/ditu/newblock?limit_offset=0&limit_count=20&discount=&search=&district=&bizcircle=&metro=&price=&sta=&ft=&room=&pro=&cycle=&fea='
cq_url_for_lianjia_city_list = 'http://cq.fang.lianjia.com/ditu/'
lianjia_second_hand_community_url_pattern = 'https://ajax.lianjia.com/ajax/mapsearch/area/community?' \
                                            'min_longitude={}&max_longitude={}&min_latitude={}&max_latitude={}' \
                                            '&&city_id={}&callback=jQuery1111026263228440180875_1502180579317&_=1502180579330'
lianjia_specific_second_hand_community_url_pattern = 'http://soa.dooioo.com/source/v4/online/house/ershoufang/listMapResult?access_token=7poanTTBCymmgE0FOn1oKp&client=pc&cityCode=sh&type=village&minLatitude={}&maxLatitude={}&minLongitude={}&maxLongitude={}&siteType=quyu'
LIANJIA_SECOND_COMMUNITY_RAW_DATA_HEADER_LIST = ['name', 'id', 'latitude', 'longitude', 'avg_unit_price', 'bs_avg_unit_price', 'house_count', 'min_price_total']
LIANJIA_SECOND_COMMUNITY_READY_DATA_HEADER_LIST = ['name', 'id', 'latitude', 'longitude', 'avg_unit_price', 'bs_avg_unit_price', 'house_count', 'min_price_total']
LIANJIA_SPECIFIC_SECOND_COMMUNITY_READY_DATA_HEADER_LIST = ['currentType', 'dataId', 'dealAvgPrice', 'latitude', 'longitude', 'saleAvgPrice', 'saleTotal', 'showName', 'sort', 'type']
LIANJIA_NEW_COMMUNITY_RAW_DATA_HEADER_LIST = ['project_name', 'resblock_id', 'latitude', 'longitude', 'average_price', 'house_type', 'rooms', 'district_id', 'resblock_frame_area',
                                              'max_frame_area','min_frame_area','price_show_config','cover_pic','show_price','show_price_desc','show_price_unit','special_tags','url']
LIANJIA_NEW_COMMUNITY_READY_DATA_HEADER_LIST = ['resblock_name', 'house_type', 'resblock_id', 'latitude', 'longitude',
                                               'average_price', 'rooms', 'resblock_frame_area', 'min_frame_area', 'max_frame_area']
LIANJIA_SPECIFIC_NEW_COMMUNITY_CITY_NAME_LIST = ['上海']
LIANJIA_SPECIFIC_SECOND_HAND_COMMUNITY_CITY_NAME_LIST = ['上海']
LIANJIA_SECOND_HAND_COMMUNITY_CITY_ID = {'北京': 110000,
                                         '重庆': 500000,
                                         '深圳': 440300,
                                         '广州': 440100,
                                         '天津': 120000,
                                         '成都': 510100,
                                         '长沙': 430100,
                                         '南京': 320100,
                                         '杭州': 330100,
                                         '武汉': 420100,
                                         '西安': 610100,
                                         '厦门': 350200}

LIANJIA_SECOND_HAND_COMMUNITY_NAME_LIST = [ 'name',
                                            'lat',
                                            'lng',
                                            'present_price',
                                            'prop_num']

LIANJIA_NEW_COMMUNITY_NAME_LIST = [ 'name',
                                    'lat',
                                    'lng',
                                    'build_type',
                                    'house_type',
                                    'start_price',
                                   ]
# fangtianxia
fangtianxia_page_url_pattern = 'http://land.fang.com/market/{}________1_0_{}.html'
fangtianxia_parcel_url_pattern = 'http://land.fang.com'
# ['重庆','北京','上海','广州','深圳','天津','成都','长沙','南京','杭州','郑州','武汉','西安','厦门']
FANGTIANXIA_CITY_NUM_TRANSFER={'北京': 110100,
                               '天津': 120100,
                               '上海': 310100,
                               '重庆': 500100,
                               '广州': 440100,
                               '深圳': 440300,
                               '成都': 510100,
                               '长沙': 430100,
                               '南京': 320100,
                               '杭州': 330100,
                               '武汉': 420100,
                               '西安': 610100,
                               '厦门': 350200,
                               }
FANGTIANXIA_PARCEL_RAW_DATA_HEADER_LIST = ['lat', 'lng', '交易地点', '交易状况', '代征面积', '位置', '保证金', '容积率',
                                           '出让年限', '出让形式', '咨询电话','商业比例','四至', '土地公告', '地区', '地块编号',
                                           '建筑密度', '建设用地面积', '总面积', '成交价' ,'成交日期','截止日期', '所在地',
                                           '最小加价幅度', '楼面地价', '溢价率', '竞得方', '绿化率', '规划建筑面积',
                                           '规划用途', '起始价', '起始日期', 	'限制高度']
FANGTIANXIA_READY_HEADER_LIST = ['地区', '总面积', '建设用地面积', '规划建筑面积', '容积率', '绿化率', '商业比例',
                                 '建筑密度', '限制高度', '出让形式','出让年限', '位置','规划用途', '起始日期',
                                 '起始价', '成交价', '楼面地价', '溢价率', 'lng', 'lat', '地块编号']


# complete data header list
COMPLETE_DATA_HEADER_LIST =['name',
                            'lat',
                            'lng',
                            'address',
                            'build_type',
                            'fitment_type',
                            'house_type',
                            'start_price',
                            'present_price',
                            'region',
                            'sub_region',
                            'prop_num',
                            'developer',
                            'category',
                            'sub_category',
                            'uid',
                            'total_area',
                            'construction_land_area',
                            'planned_land_area',
                            'floor_area_ratio',
                            'green_ratio',
                            'business_ratio',
                            'building_density',
                            'height_limit',
                            'time_limit',
                            'planned_use',
                            'start_date',
                            'land_number',
                            'data_type',
                            'city']



