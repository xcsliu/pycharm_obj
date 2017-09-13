from math import *

def calcDistance(Lat_A, Lng_A, Lat_B, Lng_B):
    ra = 6378.140  # 赤道半径 (km)
    rb = 6356.755  # 极半径 (km)
    flatten = (ra - rb) / ra  # 地球扁率
    # 转换成为弧度
    rad_lat_A = radians(Lat_A)  # adians() 方法将角度转换为弧度
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    # 对纬度对应的弧度进行校正
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    #
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))

    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return distance

# 得到当前位置单位经纬度和公里数的换算 : 1[lat] = ？[km] / 1[lng] = ？[km]
def transfer_lat_lng(Lat_A, Lng_A):
    lng_transfer = calcDistance(Lat_A, Lng_A, Lat_A, Lng_A+1)
    lat_transfer = calcDistance(Lat_A, Lng_A, Lat_A+1, Lng_A)
    return lat_transfer,lng_transfer


def get_rect_lat_lng(lat, lng, radius):
    lat_transfer, lng_transfer = transfer_lat_lng(lat, lng)
    lat_radius = radius / lat_transfer
    lng_radius = radius / lng_transfer

    min_lat = lat - lat_radius
    max_lat = lat + lat_radius
    min_lng = lng - lng_radius
    max_lng = lng + lng_radius

    return min_lng, min_lat, max_lng, max_lat

