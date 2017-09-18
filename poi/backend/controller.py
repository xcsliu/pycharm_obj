import pandas as pd

from controller.backend_controller import get_per_km_with_lat_lng

read_path = 'E:\\xcsliu_project\\pycharm_obj\\poi\\poi_data\\chongqing\\ready_data\\2017_09_18\\chongqing_insensitive_source_total_data_2017_09_18.tsv'

raw_data = pd.read_table(read_path, error_bad_lines=False, encoding = 'gbk')



def get_surrounding_total_data(lng, lat, width_KM):
    ready_data = raw_data
    dif_lat, dif_lng = get_per_km_with_lat_lng(lat, lng, width_KM)
    new_data = ready_data[(ready_data['lat'] > lat - dif_lat )&
                          (ready_data['lat'] < lat + dif_lat )&
                          (ready_data['lng'] > lng - dif_lng )&
                          (ready_data['lng'] < lng + dif_lng)]
    return new_data

