# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 12:38:15 2017

@author: xcsliu
"""
import requests
import re
import pandas as pd
import urllib
from retrying import retry
import enum



class CityCrawlerCagegory(enum.Enum):
    
    LOCATION_PATTERN_1 = '</span>位置</h3>[\s\S]*?<sup>'
    LOCATION_PATTERN_2 = '</span>位置境域</h3>[\s\S]*?<sup>'
    LOCATION_PATTERN_3 = '</span>地理环境</h2>[\s\S]*?<sup>'
    LOCATION_PATTERN_4 = '</span>地理境域</h3>[\s\S]*?<sup>'  
    LOCATION_PATTERN_5 = '</span>地理位置</h3>[\s\S]*?<sup>' 
    LOCATION_PATTERN_6 = '<div class="promotion-declaration">[\s\S]*?<sup>'
    
    LANDFORM_PATTERN = '</span>地貌</h3>[\s\S]*?<sup>'
    CLIMATE_PATTERN = '</span>气候</h3>[\s\S]*?<sup>'
    DISTRICT_PATTERN = '</span>行政区划</h2>[\s\S]*?<sup>'



class CityPicCrawler:
    def __init__(self):
        self.timeout = 5
        self.HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
        self.baike_pattern_url = 'https://baike.baidu.com/item/{}'
        self.city_list = self.get_city_name_list()
        self.saved_index_list_for_pic = []
        self.unsaved_name_list_for_pic = []   
    
    
    @retry(stop_max_attempt_number=10)
    def get_baike_text_by_city_name(self, city_name):
        baike_url = self.baike_pattern_url.format(city_name)
        response = requests.get(baike_url, headers=self.HEADERS, timeout=self.timeout)
        text = response.text    
        t = text.encode('ISO-8859-1').decode('utf8')
        return t
    
    
    def get_city_pic_url_list_by_text(self, text):
        pic_pattern = re.compile('<img src="(.*?)" />[.\n]*?<button class="picAlbumBtn">')
        res = re.findall(pic_pattern, text)        
        return res
    
    
    def get_city_name_list(self):
        read_file_path = 'E:\\poi_data\\cities.tsv'
        city_list = pd.read_table(read_file_path, error_bad_lines=False, header = None, names = ['a','b','c','d','e','f','g','h','i','j','k','l'])    
        a = city_list[city_list['c'] == 1] 
        
        c_list = []
        for idx, row in a.iterrows():
            if row['g'] == '直辖县':
                continue
            elif row['g'] != '直辖区':
                city = row['g']
                c_list.append(city)
            else:
                city = row['h'] + '市'
                c_list.append(city)
        return c_list
    
    
    def save_pic(self):
        for idx, city_name in enumerate(self.city_list):
            if idx in self.saved_index_list_for_pic:
                print (city_name+' has been saved.')
                continue
            print (idx, city_name)
            try:
                text = self.get_baike_text_by_city_name(city_name)
                img_src_list = self.get_city_pic_url_list_by_text(text)
                img_src = img_src_list[0]
                
                path_pic_pattern = 'E:\\xcsliu_project\\pycharm_obj\\city_pic_data\\{}.jpg'
                path_pic = path_pic_pattern.format(city_name)
                urllib.request.urlretrieve(img_src, path_pic)
                self.saved_index_list_for_pic.append(idx)
            except IndexError:
                self.unsaved_name_list_for_pic.append(city_name)
        if not self.unsaved_index_list_for_pic:
            path_res_record = 'E:\\xcsliu_project\\pycharm_obj\\city_pic_data\\record.txt'
            
            with open(path_res_record, 'a', encoding='utf-8') as f:
                for city_name in self.unsaved_name_list_for_pic:
                    f.write(city_name + '\n')        
                
                               
    def get_city_discription_by_text_and_category_pattern_str(self, text, pattern_str):
        pattern = re.compile(pattern_str)
        tmp_res = re.findall(pattern, text)
        try:
            t_tmp = tmp_res[0]
            
            pattern = re.compile('>(.*?)<')
            res = re.findall(pattern, t_tmp)
            
            text_description = ''.join(res[1:])
            return text_description
        except:
            return ''

    
    def get_description(self, city_name):
        
        text = self.get_baike_text_by_city_name(city_name)
        text_location_1 = self.get_city_discription_by_text_and_category_pattern_str(text, CityCrawlerCagegory.LOCATION_PATTERN_1.value)   
        text_location_2 = self.get_city_discription_by_text_and_category_pattern_str(text, CityCrawlerCagegory.LOCATION_PATTERN_2.value) 
        text_location_3 = self.get_city_discription_by_text_and_category_pattern_str(text, CityCrawlerCagegory.LOCATION_PATTERN_3.value) 
        text_location_4 = self.get_city_discription_by_text_and_category_pattern_str(text, CityCrawlerCagegory.LOCATION_PATTERN_4.value) 
        text_location_5 = self.get_city_discription_by_text_and_category_pattern_str(text, CityCrawlerCagegory.LOCATION_PATTERN_5.value) 
        text_location_6 = self.get_city_discription_by_text_and_category_pattern_str(text, CityCrawlerCagegory.LOCATION_PATTERN_6.value) 
             
        text_location = text_location_1 or text_location_2 or text_location_3 or text_location_4 or text_location_5 or text_location_6

        if text_location == '':
            path_txt_pattern = 'E:\\xcsliu_project\\pycharm_obj\\city_description_data\\empty_{}.txt'  
        else:
            path_txt_pattern = 'E:\\xcsliu_project\\pycharm_obj\\city_description_data\\{}.txt'
        path_txt = path_txt_pattern.format(city_name)

        with open(path_txt, 'a', encoding='utf-8') as f:
            f.write(text_location + '\n')
        
                
    def save_location_description(self):
        for idx, city_name in enumerate(self.city_list):
            city_name = city_name.replace('臺','台')
            print (idx, city_name)
            try:
                self.get_description(city_name)
            except IndexError:
                pass
            
            
if __name__ == '__main__':            
    CityCrawler = CityPicCrawler()              
    # CityCrawler.save_pic()
    CityCrawler.save_location_description()
    

'''
path_res_record = 'E:\\xcsliu_project\\pycharm_obj\\city_pic_data\\record.txt'
with open(path_res_record, 'a', encoding='utf-8') as f:
    summary = 'total city num : {}'.format( len(CityCrawler.unsaved_name_list_for_pic)+len(CityCrawler.saved_index_list_for_pic) )
    f.write(summary + '\n') 
    f.write('saved city num : {}'.format( len(CityCrawler.saved_index_list_for_pic) ) + '\n') 
    f.write('unsaved city num : {}'.format( len(CityCrawler.unsaved_name_list_for_pic) ) + '\n') 
    f.write('unsaved city list :' + '\n')
    
    
with open(path_res_record, 'a', encoding='utf-8') as f:
    for city_name in CityCrawler.unsaved_name_list_for_pic:
        f.write(city_name + '\t')  

# ==================================


timeout = 5
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
baike_pattern_url = 'https://baike.baidu.com/item/{}'

@retry(stop_max_attempt_number=10)
def get_baike_text_by_city_name(city_name):
    baike_url = baike_pattern_url.format(city_name)
    response = requests.get(baike_url, headers=HEADERS, timeout=timeout)
    text = response.text    
    t = text.encode('ISO-8859-1').decode('utf8')
    return t


def get_city_discription_by_text_and_category_pattern(text):
    pattern = re.compile('<div class="promotion-declaration">[\s\S]*?<sup>')
    
    tmp_res = re.findall(pattern, text)
    t_tmp = tmp_res[0]
    
    pattern = re.compile('>(.*?)<')
    res = re.findall(pattern, t_tmp)
    
    text_description = ''.join(res[1:])
    return text_description

text = get_baike_text_by_city_name('上饶')

text_location = get_city_discription_by_text_and_category_pattern(text)        
# ===================================

#'''


'''
<div class="para" label-module="para">晋城市，古称<a target=_blank href="/item/%E5%BB%BA%E5%85%B4/19437466" data-lemmaid="19437466">建兴</a>、<a target=_blank href="/item/%E6%B3%BD%E5%B7%9E">泽州</a>、<a target=_blank href="/item/%E6%B3%BD%E5%B7%9E%E5%BA%9C">泽州府</a>，是山西省辖地级市，位于山西省东南部，晋豫两省接壤处，全境居于<a target=_blank href="/item/%E6%99%8B%E5%9F%8E%E7%9B%86%E5%9C%B0">晋城盆地</a>，总面积9490平方公里，自古为兵家必争之地，素有“河东屏翰、中原咽喉、三晋门户”的美誉。<sup>[1]</sup><a class="sup-anchor" name="ref_[1]_9880">&nbsp;</a>
</div><div class="para" label-module="para">晋城市是<a target=_blank href="/item/%E5%8D%8E%E5%A4%8F%E6%96%87%E5%8C%96/977438" data-lemmaid="977438">华夏文化</a>发祥地之一，两万年前便留下<a target=_blank href="/item/%E9%AB%98%E9%83%BD%E9%81%97%E5%9D%80">高都遗址</a>、塔水河、<a target=_blank href="/item/%E4%B8%8B%E5%B7%9D">下川</a>等人类遗址。是<a target=_blank href="/item/%E5%A5%B3%E5%A8%B2%E8%A1%A5%E5%A4%A9/230" data-lemmaid="230">女娲补天</a>、<a target=_blank href="/item/%E6%84%9A%E5%85%AC%E7%A7%BB%E5%B1%B1/8262" data-lemmaid="8262">愚公移山</a>、禹凿石门、<a target=_blank href="/item/%E5%95%86%E6%B1%A4">商汤</a>筹雨等神话发源地，高僧<a target=_blank href="/item/%E6%85%A7%E8%BF%9C/14451235" data-lemmaid="14451235">慧远</a>、名将<a target=_blank href="/item/%E9%99%88%E9%BE%9F">陈龟</a>、名医<a target=_blank href="/item/%E7%8E%8B%E5%8F%94%E5%92%8C">王叔和</a>、天文学家<a target=_blank href="/item/%E5%88%98%E7%BE%B2%E5%8F%9F">刘羲叟</a>、<a target=_blank href="/item/%E6%9D%8E%E4%BF%8A%E6%B0%91/11921" data-lemmaid="11921">李俊民</a>、<a target=_blank href="/item/%E9%83%9D%E7%BB%8F">郝经</a>、<a target=_blank href="/item/%E8%8D%86%E6%B5%A9/29702" data-lemmaid="29702">荆浩</a>、<a target=_blank href="/item/%E8%B4%BE%E9%B2%81">贾鲁</a>、<a target=_blank href="/item/%E9%99%88%E5%8D%9C">陈卜</a>、<a target=_blank href="/item/%E5%AD%94%E4%B8%89%E4%BC%A0">孔三传</a>、张慎言、王国光、陈廷敬等名人故里。全市现有文物总量6767处，其中国家重点文保单位66处。包括<a target=_blank href="/item/%E5%86%B6%E5%BA%95%E5%B2%B1%E5%BA%99">冶底岱庙</a>、<a target=_blank href="/item/%E9%9D%92%E8%8E%B2%E5%AF%BA/18290" data-lemmaid="18290">青莲寺</a>、<a target=_blank href="/item/%E5%B4%87%E5%AF%BF%E5%AF%BA/32438" data-lemmaid="32438">崇寿寺</a>、<a target=_blank href="/item/%E7%8E%89%E7%9A%87%E5%BA%99/72843" data-lemmaid="72843">玉皇庙</a>、<a target=_blank href="/item/%E9%98%B3%E9%98%BF%E5%8F%A4%E5%9F%8E">阳阿古城</a>、<a target=_blank href="/item/%E6%B5%B7%E4%BC%9A%E5%AF%BA/7879" data-lemmaid="7879">海会寺</a>、<a target=_blank href="/item/%E5%BC%80%E5%8C%96%E5%AF%BA/66883" data-lemmaid="66883">开化寺</a>、<a target=_blank href="/item/%E7%A8%8B%E9%A2%A2%E4%B9%A6%E9%99%A2">程颢书院</a>、<a target=_blank href="/item/%E5%B4%87%E5%AE%89%E5%AF%BA/79019" data-lemmaid="79019">崇安寺</a>、<a target=_blank href="/item/%E7%82%8E%E5%B8%9D%E9%99%B5/2953578" data-lemmaid="2953578">炎帝陵</a>、<a target=_blank href="/item/%E6%9F%B3%E6%B0%8F%E6%B0%91%E5%B1%85">柳氏民居</a>以及<a target=_blank href="/item/%E6%B9%98%E5%B3%AA%E5%8F%A4%E5%A0%A1">湘峪古堡</a>、<a target=_blank href="/item/%E5%A4%A9%E5%AE%98%E7%8E%8B%E5%BA%9C">天官王府</a>、<a target=_blank href="/item/%E7%9A%87%E5%9F%8E%E7%9B%B8%E5%BA%9C/77820" data-lemmaid="77820">皇城相府</a>、<a target=_blank href="/item/%E9%95%BF%E5%B9%B3%E4%B9%8B%E6%88%98%E9%81%97%E5%9D%80">长平之战遗址</a>群、<a target=_blank href="/item/%E7%BE%8A%E5%A4%B4%E5%B1%B1%E7%9F%B3%E7%AA%9F">羊头山石窟</a>、中华名山<a target=_blank href="/item/%E6%9E%90%E5%9F%8E%E5%B1%B1">析城山</a>、太行至尊<a target=_blank href="/item/%E7%8E%8B%E8%8E%BD%E5%B2%AD">王莽岭</a>等众多名胜古迹和自然遗产。<sup>[2-5]</sup><a class="sup-anchor" name="ref_[2-5]_9880">&nbsp;</a>
</div><div class="para" label-module="para">晋城市古为冶炼之都，有“九头十八匠”之称。是战国“阳阿古剑”产地，境内<a target=_blank href="/item/%E6%B3%BD%E5%B7%9E%E9%93%81%E5%99%A8">泽州铁器</a>、<a target=_blank href="/item/%E5%85%B0%E8%8A%B1%E7%82%AD">兰花炭</a>曾名扬海内 。<a target=_blank href="/item/%E8%9F%92%E6%B2%B3">蟒河</a>、<a target=_blank href="/item/%E5%8E%86%E5%B1%B1/46831" data-lemmaid="46831">历山</a>等保护区，生长有<a target=_blank href="/item/%E7%8C%95%E7%8C%B4">猕猴</a>、<a target=_blank href="/item/%E5%A4%A7%E9%B2%B5">大鲵</a>等惜有动物，素有山西&quot;生物资源宝库&quot;之称。<sup>[6-7]</sup><a class="sup-anchor" name="ref_[6-7]_9880">&nbsp;</a>
</div><div class="para" label-module="para">晋城市是山西省中高档铸件、电力、畜牧业基地。二广、晋侯（阳翼）、陵沁、环城高速与<a target=_blank href="/item/207%E5%9B%BD%E9%81%93">207国道</a>交织成网，太焦、嘉南及侯月铁路贯穿全境，拥有<a target=_blank href="/item/%E5%9B%BD%E5%AE%B6%E6%A3%AE%E6%9E%97%E5%9F%8E%E5%B8%82">国家森林城市</a>、<a target=_blank href="/item/%E5%9B%BD%E5%AE%B6%E5%9B%AD%E6%9E%97%E5%9F%8E%E5%B8%82">国家园林城市</a>等多项荣誉。<sup>[8-10]</sup><a class="sup-anchor" name="ref_[8-10]_9880">&nbsp;</a>
</div>
<div class="configModuleBanner">


import requests
import re
import pandas as pd
import urllib
from retrying import retry


timeout = 5
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
url = 'https://baike.baidu.com/item/晋城'

response = requests.get(url, headers=HEADERS, timeout=timeout)
text = response.text

t = text.encode('ISO-8859-1').decode('utf8')


pattern_all = re.compile('<meta name="description" content="(.*?)">')
res_discription = re.findall(pattern_all, t)



pattern_all = re.compile('<div class="para" label-module="para">(.*?)<a target=_blank href="/item/%E5%BB%BA%E5%85%B4/19437466" data-lemmaid="19437466">')
res_discription = re.findall(pattern_all, t)


# =============
pattern = re.compile(r'[\u4e00-\u9fa5，。、“”]|\d{1-5}[]')

res = re.findall(pattern, t)
# =============

pattern = re.compile(r'^<.*?')

res = re.findall(pattern, t)


# ====================================================
# 位置描述：
def get_city_location_discription_by_text(text):
    pattern = re.compile('</span>位置</h3>[\s\S]*?<sup>')
    tmp_res = re.findall(pattern, t)
    t_tmp = tmp_res[0]
    
    pattern = re.compile('>(.*?)<')
    res = re.findall(pattern, t_tmp)
    
    text_location = ''.join(res[1:])
    return text_location
# ====================================================
# 地貌：
def get_city_landform_discription_by_text(text):
    pattern = re.compile('</span>地貌</h3>[\s\S]*?<sup>')
    tmp_res = re.findall(pattern, t)
    t_tmp = tmp_res[0]
    
    pattern = re.compile('>(.*?)<')
    res = re.findall(pattern, t_tmp)
    
    text_landform =  ''.join(res[1:])
    return text_landform
# ====================================================
# 气候：
def get_city_climate_discription_by_text(text): 
    pattern = re.compile('</span>气候</h3>[\s\S]*?<sup>')
    tmp_res = re.findall(pattern, t)
    t_tmp = tmp_res[0]
    
    pattern = re.compile('>(.*?)<')
    res = re.findall(pattern, t_tmp)
    
    text_climate =  ''.join(res[1:])
    return text_climate

# ====================================================
# 行政区划：
def get_city_district_discription_by_text(text): 
    pattern = re.compile('</span>行政区划</h2>[\s\S]*?<sup>')
    tmp_res = re.findall(pattern, t)
    t_tmp = tmp_res[0]
    
    pattern = re.compile('>(.*?)<')
    res = re.findall(pattern, t_tmp)
    
    text_district = ''.join(res[1:])
    return text_district

'''


