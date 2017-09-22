# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 16:02:44 2017

@author: xcsliu
"""
import datetime

import requests
import json
import pandas as pd
import xlwt
import seaborn as sns
import matplotlib.pyplot as plt


ak = 'GEPiAH9zkDx5oy4K1Vj7Znw8zmbGhY0M'
city_name = '重庆'
timeout = 5
location_type = 'bd09ll'

steps = 30
distance_unit = 0.005
point_list = []
time_data = []
mode = 'transit'


def get_city_center():
    city_center_url = 'https://api.map.baidu.com/geocoder/v2/?address={}&output=json&ak={}'
    city_url = city_center_url.format(city_name, ak)
    try:
        r = requests.get(city_url, timeout=timeout).json()
        return r['result']['location']
    except:
        raise ConnectionError


# 通过 location 坐标，生成坐标周围一定范围内的经纬度网格信息
def get_point_by_center():
    location = get_city_center()
    lng = location['lng']  # city center [lat, lng]
    lat = location['lat']
    start_point = {'lat': lat + steps * distance_unit, 'lng': lng - steps * distance_unit}
    for i in range(2 * steps):
        for j in range(2 * steps):
            point_list.append(['%.6f' % (start_point['lat'] - distance_unit * i),
                               '%.6f' % (start_point['lng'] + distance_unit * j)])


def get_time(coordinate, destination_location, mode):
    api_addr = "http://api.map.baidu.com/direction/v1?" \
               "mode={}&" \
               "origin={}&" \
               "destination={}&" \
               "origin_region={}&" \
               "destination_region={}&" \
               "output=json&coord_type={}&" \
               "ak={}".format(mode,
                              coordinate,
                              destination_location,
                              city_name,
                              city_name,
                              location_type,
                              ak)


    req = requests.get(api_addr)
    content = req.content
    sjson = json.loads(content)
    if 'result' in sjson:
        if sjson["status"] == 0:
            if mode == "transit":
                if 'routes' in sjson['result']:
                    if 'scheme' in sjson["result"]["routes"][0]:
                        time = sjson["result"]["routes"][0]["scheme"][0]["duration"]
                    else:
                        time = sjson["result"]["routes"][0]["duration"]
                else:
                    time = 0
            else:
                if 'routes' in sjson['result']:
                    if not sjson["result"]["routes"]:
                        time = 0
                    else:
                        time = sjson["result"]["routes"][0]["duration"]
                else:
                    time = 0
        else:
            time = 0
    else:
        time = 0
    print(coordinate, time)
    return time




def save_to_xls():
    workbook = xlwt.Workbook()
    # wtable = workbook.add_sheet('{}_traffic_borderline'.format(mode), cell_overwrite_ok=True)
    wtable = workbook.add_sheet('driving_zxd_p', cell_overwrite_ok=True)
    nrows = len(point_list)
    lat = get_city_center()['lat']
    lng = get_city_center()['lng']
    city_center_location = str(lat) + ',' + str(lng)

    point_num = 1
    
    for row_num in range(nrows):
        tmp_location = str(point_list[row_num][0]) + "," + str(point_list[row_num][1])
        time = get_time(tmp_location, city_center_location, mode)
        wtable.write(row_num, 0, point_list[row_num][0])                               # row 行号
        wtable.write(row_num, 1, point_list[row_num][1])                               # xls.write(row, column, data)
        wtable.write(row_num, 2, time)
        time_data.append(int(time/60))
        print (str(point_num) + '/' + str(4*steps*steps) )   
        point_num += 1
    workbook.save('driving_zxd_p.xls')
    # workbook.save('{}_traffic_borderline_data_in_{}.xls'.format(mode, city_name))


def plot_heatmap():
    data = []
    for i in range(2*steps):
        data.append(time_data[i * (2 * steps) : (i+1) * (2 * steps)])
    pd_data = pd.DataFrame(data)
    f, ax = plt.subplots(figsize=(17, 15))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(pd_data,
                cmap=cmap,
                vmin=0,
                vmax=120,
                square=True,
                cbar_kws={"shrink": .5},
                xticklabels=False,
                yticklabels=False)


def main():
    t1 = datetime.datetime.now()
    get_point_by_center()
    save_to_xls()
    plot_heatmap()
    t2 = datetime.datetime.now()
    print (t2-t1)

if __name__ == '__main__':
    main()




