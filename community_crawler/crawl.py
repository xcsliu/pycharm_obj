#!/usr/bin/env python
# coding=utf8

import math
from json import loads
from patterns import community
from pinyin import PinYin
from run_command import run_command, MyTimeoutError
import os


def lnglat2mercator(lng, lat):
    x = lng*20037508.34/180
    y = math.log(math.tan((90+lat)*math.pi/360))/(math.pi/180)
    y = y*20037508.34/180
    return x, y


def get_surrounding_boundary(boundary):
    boundary = boundary[:-1]
    xs = [x for x, _ in boundary]
    ys = [lat for _, lat in boundary]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_mid = (x_min+x_max)/2
    y_mid = (y_min+y_max)/2
    span = max(x_max-x_min, y_max-y_min)
    sw = [x_mid-span, y_mid-span]
    nw = [x_mid-span, y_mid+span]
    se = [x_mid+span, y_mid-span]
    ne = [x_mid+span, y_mid+span]
    exterior_boundary = [sw, se, ne, nw, sw]
    distance_to_sw = lambda x, y: ((x-x_min)**2+(y-y_min)**2)**0.5
    index = None
    d_min = distance_to_sw(x_max, y_max)
    for i, (x, y) in enumerate(boundary):
        d = distance_to_sw(x, y)
        if d < d_min:
            index = i
            d_min = d
    interior_boundary = boundary[index:]+boundary[:index+1]
    surrounding_boundary = exterior_boundary+interior_boundary+[sw]
    return surrounding_boundary


def crawl(i, city, name, boundary):
    boundary = [[round(lng, 6), round(lat, 6)] for lng, lat in boundary]
    lngs = [lng for lng, _ in boundary]
    lats = [lat for _, lat in boundary]
    lng_min, lng_max = min(lngs), max(lngs)
    lat_min, lat_max = min(lats), max(lats)
    lng_center = round((lng_min+lng_max)/2, 6)
    lat_center = round((lat_min+lat_max)/2, 6)
    x_min, y_min = [math.floor(v) for v in lnglat2mercator(lng_min, lat_min)]
    x_max, y_max = [math.floor(v) for v in lnglat2mercator(lng_max, lat_max)]
    span = max(x_max-x_min, y_max-y_min)
    center = "%.6f, %.6f" % (lng_center, lat_center)
    interior_boundary = boundary
    surrounding_boundary = get_surrounding_boundary(boundary)
    surrounding_boundary = ["new BMap.Point(%f, %f)" % (lng, lat) for lng, lat in surrounding_boundary]
    surrounding_boundary = ",\n        ".join(surrounding_boundary)
    # print("make html")
    html = "html/%d-%s-%s.html" % (i, city, name)
    f = open(html, "w", encoding="utf8")
    f.write(community % {"center": center, "surrounding_boundary": surrounding_boundary})
    f.close()
    # print("render html and save png")
    html = "file:///D:/community_crawler/%s" % html
    png = "png/%d-%s-%s.png" % (i, city, name)
    cmd = "phantomjs crawl.js %d %s %s" % (span, html, png)
    print(cmd)
    # os.system(cmd)
    try:
        run_command(cmd, 10)
    except MyTimeoutError:
        print("excute command=<%s> timeout after %i' % (cmd, timeout)")


p = PinYin()
p.load_word()


def hanzi2pinyin(hanzi_str):
    pinyin_str = "".join(p.hanzi2pinyin(string=hanzi_str))
    return pinyin_str


def test():
    city = "深圳"
    name = "富通城-一期"
    city = hanzi2pinyin(city)
    name = hanzi2pinyin(name)
    boundary = [[113.69549455128, 22.817687794172], [113.69552587879, 22.818009544586], [113.69570240211, 22.818228674736], [113.69767083741, 22.818400147483], [113.69787782766, 22.816793427024], [113.69752857277, 22.816685596896], [113.69671903332, 22.816502415591], [113.69592205487, 22.816370254703], [113.69549455128, 22.817687794172]]
    crawl(1, city, name, boundary)


def main():
    for i, line in enumerate(open("community.tsv", "r", encoding="utf8")):
        city, name, boundary = line.strip("\n").split("\t")
        if i < 26618:
            continue
        print(i, city, name)
        city = hanzi2pinyin(city)
        try:
            name = hanzi2pinyin(name)
        except:
            name = "none"
        if name[-3:] == "lou" or name[-5:] == "dasha" or name[-6:] == "gongyu":
            continue
        boundary = loads(boundary)
        crawl(i, city, name, boundary)


if __name__ == "__main__":
    # test()
    main()
