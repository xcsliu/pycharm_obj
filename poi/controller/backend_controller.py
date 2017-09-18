import pandas as pd


read_path = 'E:\\xcsliu_project\\pycharm_obj\\poi\\poi\\poi_data\\chongqing\\ready_data\\2017_09_15\\chongqing_2017_09_15.tsv'
raw_data = pd.read_table(read_path, error_bad_lines=False, encoding = 'gbk')




from math import radians, cos, sin, asin, sqrt  
  
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）  
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """  
    # 将十进制度数转化为弧度  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
  
    # haversine公式  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里  
    return c * r * 1000  





# ======================
# 换算该 经纬度 位置, 1经度对应的公里数
def haversine_lng(lng1, lat1): # 经度1，纬度1，经度2，纬度2 （十进制度数）  
    lng2 = lng1 + 1 
    lat2 = lat1
    # 将十进制度数转化为弧度  
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])  
  
    # haversine公式  
    dlng = lng2 - lng1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里  
    return c * r 

# 换算该 经纬度 位置, 1纬度对应的公里数
def haversine_lat(lng1, lat1): # 经度1，纬度1，经度2，纬度2 （十进制度数）  
    lng2 = lng1 
    lat2 = lat1 + 1 
    # 将十进制度数转化为弧度  
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])  
  
    # haversine公式  
    dlng = lng2 - lng1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里  
    return c * r   



def get_per_km_with_lat_lng(lat, lng, width_KM):

    def convert_lng(lng1, lat1):
        lng2 = lng1 + 1
        lat2 = lat1
        # 将十进制度数转化为弧度
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
        # haversine公式
        dlng = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # 地球平均半径，单位为公里
        return c * r

    def convert_lat(lng1, lat1):
        lng2 = lng1
        lat2 = lat1 + 1
        # 将十进制度数转化为弧度
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
        # haversine公式
        dlng = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # 地球平均半径，单位为公里
        return c * r

    ratio_lat = convert_lat(lng, lat)
    ratio_lng = convert_lng(lng, lat)

    dif_lat = width_KM / ratio_lat / 2
    dif_lng = width_KM / ratio_lng / 2

    return dif_lat, dif_lng
# ======================







def get_nearby_data(raw_data, lng, lat, width_KM):     
    dif_lat_per_km, dif_lng_per_km = get_per_km_with_lat_lng(lat, lng, width_KM)
    dif_lat = dif_lat_per_km * width_KM
    dif_lng = dif_lng_per_km * width_KM
    
    new_data = raw_data[(raw_data['lat'] > lat - dif_lat)&
                        (raw_data['lat'] < lat + dif_lat)&
                        (raw_data['lng'] > lng - dif_lng)&
                        (raw_data['lng'] < lng + dif_lng)]
    return new_data


    
filtered_data = get_nearby_data(raw_data, 106.521808, 29.580044, 1)


import time

def get_yesterday():
    delta_time = 60*60*24
    t = time.time() - delta_time
    yesterday = time.strftime('%Y_%m_%d', time.localtime(t))
    return yesterday



    
print (get_yesterday())    
    





# ======================











