class PoiData:
    def __init__(self):     # 不易区分的，给一个区分的例子
        # 基本信息
        self.name = None                   # 名称
        self.lat = None                    # 纬度
        self.lng = None                    # 经度
        self.address = None                # 地址
        # 小区/楼盘 信息
        self.building_type = None          # 建筑类型
        self.fitment_type = None           # 装修类型
        self.apartment_layout_type = None  # 户型
        self.initial_price = None          # 开盘价格
        self.present_price = None          # 当前价格
        self.region = None                 # 地区
        self.sub_region = None             # 细分地区
        self.property_onsale_count = None  # 在售数目
        self.developer = None              # 开发商
        # 百度 poi 信息
        self.category = None               # 分类
        self.sub_category = None           # 细分类
        self.baidu_uid = None              # 百度uid
        # 地块信息
        self.total_area = None             # 总面积
        self.construction_land_area = None # 建设用地面积
        self.planned_land_area = None      # 计划用地面积
        self.floor_area_ratio = None       # 容积率
        self.green_ratio = None            # 绿化率
        self.business_ratio = None         # 商业比例
        self.building_density = None       # 建筑密度
        self.height_limit = None           # 高度限制
        self.term_limit = None             # 时间限制(土地出让年限)
        self.planned_usage = None          # 计划用途
        self.start_date = None             # 开始时间(土地出让起始时间/楼盘开盘时间)
        self.land_block_number = None      # 地块编号
        self.data_type = None              # 数据类型
        self.city = None                   # 所在城市



