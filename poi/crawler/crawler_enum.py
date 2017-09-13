import enum

class CrawlerSourceName(enum.Enum):
    ANJUKE = 'anjuke'
    LIANJIA = 'lianjia'
    BAIDU = 'baidu'
    FANGTIANXIA = 'fangtianxia'


class CrawlerDataType(enum.Enum):
    RAW_DATA = 'raw_data'
    READY_DATA = 'ready_data'


class CrawlerDataLabel(enum.Enum):
    SECOND_HAND_COMMUNITY = 'second_hand_community'
    NEW_COMMUNITY = 'new_community'
    BAIDU_POI = 'poi'
    PARCEL = 'parcel'
    SINGLE_SECOND_HAND_APARTMENT = 'second_hand_apartment'